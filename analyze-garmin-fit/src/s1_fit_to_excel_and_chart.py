# ruff: noqa: PD008 PLR2004 FBT003
"""
Convert Fit file to Excel and plot chart.

reads .fit file
converts into 2 Pandas Dataframes : lap summary and points
filter on interesting columns
converts to local time
export as Excel sheets
plot charts

see https://towardsdatascience.com/parsing-fitness-tracker-data-with-python-a59e7dc17418
and
https://github.com/bunburya/fitness_tracker_data_parsing/blob/main/parse_fit.py
"""

import os
import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING

import fitdecode  # pip install fitdecode
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    import datetime as dt

file_in = "data/231111.fit"

# ensure working dir is script dir
os.chdir(Path(sys.argv[0]).parent)

warnings.filterwarnings("ignore", message=".*native_field_num.*not found in message.*")

# The names of the columns we will use in our points DataFrame.
POINTS_COLUMN_NAMES = [
    "timestamp",
    # "altitude",
    "enhanced_altitude",
    "ascent",
    # "battery_soc",
    "cadence",
    "calories",
    "descent",
    "distance",
    # "gps_accuracy",
    "grade",
    "heart_rate",
    "latitude",
    "longitude",
    # "position_lat",
    # "position_long",
    # "speed",
    "enhanced_speed",
    "temperature",
]

# The names of the columns we will use in our laps DataFrame.
LAPS_COLUMN_NAMES = [
    "start_time",
    "timestamp",  # = end of lap
    # "avg_altitude",
    "enhanced_avg_altitude",
    "avg_cadence",
    "avg_grade",
    "avg_heart_rate",
    # "avg_speed",
    "enhanced_avg_speed",
    "avg_temperature",
    # "event",
    # "event_type",
    # "max_altitude",
    "enhanced_max_altitude",
    "max_cadence",
    "max_heart_rate",
    "max_neg_grade",
    "max_pos_grade",
    # "max_speed",
    "enhanced_max_speed",
    # "max_temperature",
    # "min_altitude",
    "enhanced_min_altitude",
    "min_heart_rate",
    # "time_in_hr_zone",
    "total_ascent",
    "total_calories",
    "total_descent",
    "total_distance",
    # "total_elapsed_time",
    "total_timer_time",  # = active time
]


def get_fit_lap_data(
    frame: fitdecode.records.FitDataMessage,
) -> dict[str, float | dt.datetime | dt.timedelta | int]:
    """
    Get fit lab data.

    Extract some data from a FIT frame representing a lap and return
    it as a dict.
    """
    data: dict[str, float | dt.datetime | dt.timedelta | int] = {}

    for field in LAPS_COLUMN_NAMES:
        if frame.has_field(field):
            data[field] = frame.get_value(field)  # type: ignore

    return data


def get_fit_point_data(
    frame: fitdecode.records.FitDataMessage,
) -> dict[str, float | int | str | dt.datetime] | None:
    """
    Get point data from .fit file.

    Extract some data from an FIT frame representing a track point
    and return it as a dict.
    """
    data: dict[str, float | int | str | dt.datetime] = {}

    if not (frame.has_field("position_lat") and frame.has_field("position_long")):
        # Frame does not have any latitude or longitude data.
        # We will ignore these frames in order to keep things simple
        return None

    data["latitude"] = frame.get_value("position_lat") / ((2**32) / 360)  # type: ignore
    data["longitude"] = frame.get_value("position_long") / ((2**32) / 360)  # type: ignore

    for field in POINTS_COLUMN_NAMES:
        if frame.has_field(field):
            data[field] = frame.get_value(field)  # type: ignore
    return data


def get_dataframes(file_in: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Get DFs.

    Takes the path to a FIT file (as a string) and returns two Pandas
    DataFrames: one containing data about the laps, and one containing
    data about the individual points.
    """
    points_data = []
    laps_data = []
    lap_no = 1
    with fitdecode.FitReader(file_in) as fit_file:
        for frame in fit_file:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                if frame.name == "record":
                    single_point_data = get_fit_point_data(frame)
                    if single_point_data is not None:
                        single_point_data["lap"] = lap_no
                        points_data.append(single_point_data)
                elif frame.name == "lap":
                    single_lap_data = get_fit_lap_data(frame)
                    single_lap_data["number"] = lap_no
                    laps_data.append(single_lap_data)
                    lap_no += 1

    # Create DataFrames from the data we have collected.
    # If any information is missing from a particular lap or track
    # point, it will show up as a null value or "NaN" in the DataFrame.

    df_laps = pd.DataFrame(laps_data, columns=LAPS_COLUMN_NAMES)
    df_points = pd.DataFrame(points_data, columns=POINTS_COLUMN_NAMES)
    return df_laps, df_points


def df_finetuning_laps(df: pd.DataFrame) -> pd.DataFrame:
    """Finetuning."""
    df = df_finetuning(df)
    # add lap counter as first column
    df.index.name = "lap"
    df = df.reset_index(level=0)
    df["lap"] += 1
    return df


def df_finetuning_points(df: pd.DataFrame) -> pd.DataFrame:
    """Finetuning."""
    df = df_finetuning(df)
    return df


def df_finetuning(df: pd.DataFrame) -> pd.DataFrame:
    """Column renaming and timezone localization."""
    df.columns = df.columns.str.replace("enhanced_", "")
    df = df_remove_timezone_info(df=df, local_timezone="Europe/Berlin")
    return df


def df_remove_timezone_info(
    df: pd.DataFrame, local_timezone: str = "Europe/Berlin"
) -> pd.DataFrame:
    """
    Convert to local time.

    and remove timezone offset info because Excel cannot handle it
    """
    date_columns = ("start_time", "timestamp")
    for c in date_columns:
        if c in df.columns:
            df[c] = (
                df[c]
                # .dt.tz_localize("utc")
                .dt.tz_convert(tz=local_timezone)  # type: ignore
                .dt.tz_localize(None)
            )
    return df


def calc_df_km(  # noqa: PLR0915
    df_points: pd.DataFrame, pause_threshhold: float = 3.6 / 4
) -> pd.DataFrame:
    """
    Calc kilometers.

    removes pauses
    via making use of the 1s resolution in the data
    dropping all slow speed points
    remaining number of rows * 1s = movement time
    pause_threshhold in m/s, default: 0.25km/h (3.6/4)
    """
    cols_av = ["altitude", "cadence", "grade", "heart_rate", "speed", "temperature"]
    cols_sum = ["ascent", "descent"]
    cols_max = ["calories", "distance"]
    l_ = cols_av
    l_.extend(cols_sum)
    l_.extend(cols_max)
    for c in l_:
        assert c in df_points.columns, c

    # filter out pause speed < pause_threshhold
    df = df_points[df_points["speed"] > pause_threshhold]
    df = df.reset_index(drop=True)
    df.index.name = "time_moving"
    # index -> column
    df = df.reset_index(level=0)

    df = df.rename(
        columns={
            "distance": "distance_total",
            "ascent": "ascent_total",
            "descent": "descent_total",
        },
        errors="raise",
    )

    # zero fill missing values
    df["distance_total"] = df["distance_total"].fillna(0)
    df["ascent_total"] = df["ascent_total"].fillna(0)
    df["descent_total"] = df["descent_total"].fillna(0)
    df["heart_rate"] = df["heart_rate"].fillna(0)

    # remove offset by subtracting first data point
    df["distance_total"] -= df["distance_total"].iloc[0]
    df["ascent_total"] -= df["ascent_total"].iloc[0]
    df["descent_total"] -= df["descent_total"].iloc[0]
    df["calories"] -= df["calories"].iloc[0]

    df["km_lap"] = 1 + df["distance_total"] / 1000
    df["km_lap"] = df["km_lap"].astype("int")
    df = df.groupby(["km_lap"]).agg(
        {
            "time_moving": "max",
            "distance_total": "max",
            "heart_rate": "mean",
            "ascent_total": "max",
            "descent_total": "max",
        },
    )

    df["km"] = df["distance_total"] / 1000

    df["distance_delta"] = df["distance_total"].diff()
    df.at[df.index[0], "distance_delta"] = df["distance_total"].iloc[df.index[0]]
    df["time_delta"] = df["time_moving"].diff()
    df.at[df.index[0], "time_delta"] = df["time_moving"].iloc[df.index[0]]
    # calc speed
    # df["m/s"] = df["distance_delta"] / df["time_delta"]
    df["km/h"] = df["distance_delta"] / df["time_delta"] * 3.6

    # calc ascent and descent
    df["ascent"] = df["ascent_total"].diff()
    df.at[df.index[0], "ascent"] = df["ascent_total"].iloc[df.index[0]]
    df["descent"] = df["descent_total"].diff()
    df.at[df.index[0], "descent"] = df["descent_total"].iloc[df.index[0]]
    df["elevation"] = (df["ascent"] - df["descent"]) / df["distance_delta"] * 1000

    # heat_rate per km/h
    # subtracting a resting HR of 50 first
    hr_resting = 50
    df["hr/kmh"] = (df["heart_rate"] - hr_resting) / df["km/h"]

    # remove this where ascent is too high
    df.loc[(df.ascent > 10), "hr/kmh"] = np.nan
    df.loc[(df.descent > 10), "hr/kmh"] = np.nan
    # remove first and last data point
    df.at[df.index[0], "hr/kmh"] = np.nan
    df.at[df.index[-1], "hr/kmh"] = np.nan

    # rounding and int conversion
    df["distance_delta"] = df["distance_delta"].dropna().astype("int")
    df["distance_total"] = df["distance_total"].dropna().astype("int")
    df["km"] = df["km"].round(1)
    df["time_moving"] = df["time_moving"].dropna().astype("int")
    df["time_delta"] = df["time_delta"].dropna().astype("int")
    df["heart_rate"] = df["heart_rate"].dropna().round(1)
    # df["m/s"] = df["m/s"].round(1)
    df["km/h"] = df["km/h"].dropna().round(1)

    df["ascent"] = df["ascent"].dropna().astype("int")
    df["descent"] = df["descent"].dropna().astype("int")
    df["elevation"] = df["elevation"].dropna().round(1).astype("int")
    df["ascent_total"] = df["ascent_total"].dropna().astype("int")
    df["descent_total"] = df["descent_total"].dropna().astype("int")

    # df["hr/kmh"] =

    # df.drop(columns=["m/s"], inplace=True)

    df = df.reset_index(level=0)
    df = df.set_index(["km"])
    return df


def export_excel(
    df_laps: pd.DataFrame, df_points: pd.DataFrame, df_km: pd.DataFrame
) -> None:
    """Export as Excel file."""
    writer = pd.ExcelWriter(file_in.replace(".fit", ".xlsx"), engine="xlsxwriter")
    df_km.to_excel(writer, sheet_name="km", index=False)
    df_points.to_excel(writer, sheet_name="Points", index=False)
    df_laps.to_excel(writer, sheet_name="Laps", index=False)
    writer.close()


def plot_km_chart_lines(df: pd.DataFrame) -> None:
    """Plot km chart with lines."""
    # initialize plot
    _fig, ax = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        figsize=(6, 8),  # default: 6.4,4.8
        dpi=100,
        # smaller plot 1, larger plot 2
        gridspec_kw={"width_ratios": [1], "height_ratios": [1, 3]},
    )

    # df["elevation"].plot.bar(ax=ax[0], color="green", width=1.0)
    df["elevation"].plot(ax=ax[0], color="green")
    ax[0].set_ylabel("elevation (m/km)", color="green")
    ax[0].tick_params(axis="y", colors="green")
    df["km/h"].plot(ax=ax[1], color="blue")
    ax[1].set_ylabel("km/h", color="blue")
    ax[1].tick_params(axis="y", colors="blue")
    df["heart_rate"].plot(ax=ax[1], secondary_y=True, color="red")
    ax[1].right_ax.set_ylabel("heart rate", color="red")
    ax[1].right_ax.tick_params(axis="y", colors="red")
    # ax[0].set_xticks()

    ax[0].tick_params(
        axis="x",
        bottom=False,
        top=True,
        labelbottom=False,
        labeltop=True,
    )
    ax[0].grid(zorder=0, axis="both")
    ax[1].tick_params(
        axis="x",
        bottom=True,
        top=False,
        labelbottom=True,
        labeltop=False,
    )
    ax[1].grid(zorder=0, axis="both")
    ax[1].right_ax.grid(None)

    ax[1].grid(True)
    ax[1].set_axisbelow(True)

    plt.grid(axis="both")
    plt.tight_layout()
    plt.savefig(file_in=file_in.replace(".fit", "-plot-lines.png"), format="png")
    plt.clf()
    plt.close()


def plot_km_chart_bars(df: pd.DataFrame) -> None:
    """Plot km chart with bars."""
    # colors = list(mcolors.TABLEAU_COLORS.keys())
    colors = ("tab:blue", "tab:red", "tab:orange", "tab:brown")
    # initialize plot
    _fig, ax = plt.subplots(
        nrows=1,
        ncols=4,
        sharey=True,
        figsize=(10.8, 19.2),
        dpi=100,
        # smaller plot 1, larger plot 2
        # gridspec_kw={"width_ratios": [1, 1, 1,1], "height_ratios": [1]},
    )

    series_to_plot = ["km/h", "heart_rate", "hr/kmh", "elevation"]

    y_values = range(1, len(df.index) + 1)
    for series_no in range(len(series_to_plot)):
        series_name = series_to_plot[series_no]

        # plot
        ax[series_no].barh(
            y_values,
            df[series_name],
            align="center",
            color=colors[series_no],
        )

        # title
        ax[series_no].set_title(series_name, color=colors[series_no])

        # grid and mean line
        # ax[series_no].grid(axis="x")
        ax[series_no].grid(axis="both")  # , zorder=-1
        ax[series_no].set_axisbelow(True)  # for grid below the lines

        ax[series_no].axvline(
            df[series_name].mean(),
            color="gray",
            ls="--",
        )

        # auto-scale value range
        low = df[series_name].min()
        high = df[series_name].max()
        ax[series_no].set_xlim(int(low - 1), int(high + 1))

    # remove tics for chart 2..
    for series_no in range(1, len(series_to_plot)):
        ax[series_no].tick_params(
            axis="y",
            # bottom=False,
            # top=False,
            # labelbottom=False,
            # labeltop=False,
            left=False,
            labelleft=False,
            right=False,
            labelright=False,
        )

    # for series_no in range(len(series_to_plot)):
    # ax[series_no].tick_params(axis="x", color=colors[series_no])
    # ax[series_no].xaxis.label.set_color(colors[series_no])

    ax[0].set_ylabel("distance (km)", loc="center")

    # y range (exclude 0)
    ax[0].set_ylim(0.5, len(y_values) + 0.5)

    # layout
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.tight_layout()
    plt.savefig(file_in=file_in.replace(".fit", "-plot-bars.png"), format="png")
    plt.close()


if __name__ == "__main__":
    df_laps, df_points = get_dataframes(file_in)
    df_laps = df_finetuning_laps(df=df_laps)
    df_points = df_finetuning_points(df=df_points)
    df_km = calc_df_km(df_points)
    # df_km.rename(
    #     columns={
    #         "heart_rate": "HR",
    #     },
    #     errors="raise",
    #     inplace=True,
    # )
    plot_km_chart_bars(df=df_km)
    # plot_km_chart_lines(df=df_km)

    # print("LAPS:")
    # print(df_laps)
    # print("\nPOINTS:")
    # print(df_points)

    # export_excel(df_laps=df_laps, df_points=df_points, df_km=df_km)
