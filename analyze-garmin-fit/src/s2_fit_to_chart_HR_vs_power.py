"""
.fit to chart of heart rate vs. power.

read .fit files in data/
convert to Pandas DataFrame
plot raw data of power and heart rate vs. time
export raw data as Excel sheet
group by power
plot heart rate vs. power

only use for comparative tracks, preferable power ramps
"""

import datetime as dt  # noqa: TC003
import os
import sys
from pathlib import Path

import fitdecode  # pip install fitdecode # type: ignore
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colormaps  # type: ignore
from matplotlib.ticker import MultipleLocator  # df.index.max()

# ensure working dir is script dir
os.chdir(Path(sys.argv[0]).parent)

FIT_COLUMN_NAMES = ("timestamp", "power", "heart_rate", "cadence")
ROUND_TO_WATT = 20
MIN_VALUES_PER_WATT = 20
# for Excel export
TIMEZONE_LOCAL = "Europe/Berlin"


def load_fit_data(file_in: Path) -> pd.DataFrame:
    """
    Load data from .fit file as DataFrame.

    parse only "record" data point, not lap aggregation
    """
    points_data = []
    with fitdecode.FitReader(file_in) as fit_file:
        for frame in fit_file:
            if (
                isinstance(frame, fitdecode.records.FitDataMessage)
                and frame.name == "record"  # type: ignore
            ):
                data: dict[str, float | int | dt.datetime] = {}

                for field in frame.fields:  # type: ignore
                    # only relevant fields
                    if field.name in FIT_COLUMN_NAMES:  # type: ignore
                        data[field.name] = field.value  # type: ignore
                points_data.append(data)  # type: ignore
    # print(points_data)
    df = pd.DataFrame(points_data)
    # print (df)
    return df


def clean_and_prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare data.

    drop points with missing or too low data
    add elapsed time
    filter out 1st minute
    round power to 20W
    """
    # drop points with missing data
    df = df.dropna(subset=["power", "heart_rate", "cadence"])  # type: ignore

    # drop points with too low data
    df = df.query("power >= 80 & cadence >= 40")  # type: ignore

    df = df.rename(
        columns={"timestamp": "datetime"},
    )

    # convert datetime to timestamp
    df["timestamp"] = df["datetime"].astype(int) // 10**9  # type: ignore # //: integer division

    # calc elapsed time
    df["seconds"] = df["timestamp"] - df["timestamp"].iloc[0]  # type: ignore

    # filter out first 1min
    df = df.query("seconds > 1 * 60")  # type: ignore

    # use seconds as index
    df = df.set_index("seconds")  # type: ignore

    # round power to 20W
    df["power_rounded"] = df["power"].apply(  # type: ignore
        lambda x: custom_round(x, base=ROUND_TO_WATT),  # type: ignore
    )
    # print(df)
    return df


def custom_round(x: float, base: int = 5) -> int:
    """Round to certain base."""
    # from https://stackoverflow.com/questions/40372030/pandas-round-to-the-nearest-n
    return int(base * round(float(x) / base))


def df_to_excel(df: pd.DataFrame) -> None:
    """
    Excel export.

    timezone is dropped from datetime, as Excel can not handle timezone information
    """
    df["datetime"] = (
        df["datetime"].dt.tz_convert(tz=TIMEZONE_LOCAL).dt.tz_localize(None)  # type: ignore
    )
    writer = pd.ExcelWriter(path=file_in.with_suffix(".xlsx"))
    df.to_excel(writer, sheet_name="Points", index=True)  # type: ignore
    writer.close()


def plot_hr_vs_time(df: pd.DataFrame, file_in: Path) -> None:
    """
    Plot activity.

    plot heart_rate and power over seconds, use hear_rate as secondary axis
    """
    colors = ("tab:blue", "tab:red")  # tableau colors blue and red
    _fig, ax = plt.subplots(nrows=1, ncols=1)  # type: ignore
    max_watt: float = df["power"].max()  # type: ignore
    df["power"].plot(
        ax=ax,
        label="Power",
        secondary_y=False,
        legend=False,
        color=colors[0],
    )
    plt.yticks(range(100, int(max_watt + 1), 40))  # type: ignore
    ax.yaxis.set_minor_locator(MultipleLocator(20))

    plt.grid(axis="both")  # type: ignore
    df["heart_rate"].plot(
        ax=ax,
        label="Heart Rate",
        secondary_y=True,
        legend=False,
        color=colors[1],
    )
    ax.set_xlabel("Time (min)")  # type: ignore
    ax.set_ylabel("Power (W)", color=colors[0])  # type: ignore
    ax.yaxis.label.set_color(colors[0])  # type: ignore
    ax.tick_params(axis="y", colors=colors[0])  # type: ignore
    ax.right_ax.set_ylabel("Heart Rate (bpm)", color=colors[1])  # type: ignore
    ax.right_ax.yaxis.label.set_color(colors[1])  # type: ignore
    ax.right_ax.tick_params(axis="y", colors=colors[1])  # type: ignore

    seconds = np.arange(0, df.index.max() + 120, 120)  # type: ignore
    minutes = seconds // 60  # // = integer division# type: ignore

    plt.xticks(ticks=seconds, labels=minutes)  # type: ignore

    ax.xaxis.set_minor_locator(MultipleLocator(60))

    plt.tight_layout()  # type: ignore
    plt.savefig(fname=file_in.with_suffix(".png"), format="png")  # type: ignore


def plot_all_df2s(list_df: list[pd.DataFrame], files: list[Path]) -> None:
    """Plot the calculated dataframes of HR vs. Watt."""
    _fig, ax = plt.subplots(  # type: ignore
        nrows=1,
        ncols=1,
    )
    # Get the blue to red colormap
    colormap = colormaps["coolwarm"]  # type: ignore
    colors = [colormap(i / len(files)) for i in range(len(files))]  # type: ignore

    for i in range(len(files)):
        file_in = files[i]
        df = list_df[i]

        df["heart_rate"].plot(
            ax=ax,
            legend=True,
            label=file_in.stem,
            color=colors[i],
            linewidth=3.0,
        )

    # plt.legend()  # type: ignore
    plt.xticks(range(100, max_watt, 40))  # type: ignore
    # set minor ticks to every 20
    ax.xaxis.set_minor_locator(MultipleLocator(20))
    ax.set_xlim(100, max_watt)

    plt.xlabel("Power (W)")  # type: ignore
    plt.ylabel("Heart Rate (bpm)")  # type: ignore
    plt.grid(axis="both")  # type: ignore
    plt.tight_layout()  # type: ignore
    plt.savefig(fname="hr_vs_watt.png", format="png")  # type: ignore


def doit(file_in: Path) -> pd.DataFrame:
    """Do it."""
    df = load_fit_data(file_in)
    df = clean_and_prepare_data(df)
    plot_hr_vs_time(df=df, file_in=file_in)
    # df_to_excel(df=df)

    # group by power
    df2 = df.groupby(["power_rounded"]).agg(  # type: ignore
        {
            "heart_rate": "mean",
            "cadence": "mean",
            "power": "count",
        },
    )
    df2.index.name = "power"  # type: ignore
    df2 = df2.rename(columns={"power": "count"})

    # filter out Watts with too few values
    df2 = df2[df2["count"] >= MIN_VALUES_PER_WATT]

    print(df2)
    return df2


if __name__ == "__main__":
    max_watt = 0
    files = sorted(Path("data").glob("*.fit"))
    list_df: list[pd.DataFrame] = []

    for file_in in files:
        print(file_in)
        df = doit(file_in)
        list_df.append(df)
        max_watt = max(max_watt, df.index.max())  # type: ignore
    plot_all_df2s(list_df, files)
