"""Read the InfluxDB Shelly data and convert it to JSON."""

import csv
import datetime as dt
from pathlib import Path

from helper import append_data, export_json

FILE_IN = Path("data/influx-media.csv")
# example:
# datetime	ShellyNo	watt_now
# 2025-06-03 17:05:00	3	120.8

DURATION_MIN = 10


def guess_activity(watt: float) -> str:
    """Guess activity based on watt."""
    # gaming 3D: 450W
    # movie: 207W
    # PC, non gaming?
    # gaming 2D?

    if watt <= 50:  # noqa: PLR2004
        return "idle"
    if watt >= 207 - 30 and watt <= 207 + 30:
        return "movie"
    if watt >= 450:  # noqa: PLR2004
        return "gaming 3D+"
    if watt >= 320:  # noqa: PLR2004
        return "gaming 3D-"
    if watt >= 260:  # noqa: PLR2004
        return "gaming 2D"
    return "unknown" + str(round(watt / 10) * 10)


def read_data_to_list(file_in: Path) -> list[tuple[dt.datetime, float]]:
    """Read influx.csv and return list."""
    # d: dict[str, list[str]] = {}
    lst: list[tuple[dt.datetime, float]] = []
    with file_in.open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            # 2025-06-03 17:05:00
            my_dt = dt.datetime.fromisoformat(row["datetime"])
            lst.append((my_dt, float(row["watt_now"])))
            # date = str(my_dt.date())
            # time = my_dt.strftime("%H:%M")
            # s = time
            # append_data(d, date, s)
    return lst


def moving_average(
    lst: list[tuple[dt.datetime, float]],
) -> list[tuple[dt.datetime, float]]:
    """Apply rolling average of 3 values if datetime difference < 2.5min."""
    if len(lst) < 3:  # noqa: PLR2004
        return lst
    result: list[tuple[dt.datetime, float]] = []
    for i in range(len(lst)):
        if i == 0 or i == len(lst) - 1:
            result.append(lst[i])
            continue
        prev_dt, prev_val = lst[i - 1]
        curr_dt, curr_val = lst[i]
        next_dt, next_val = lst[i + 1]
        if (curr_dt - prev_dt).total_seconds() <= 150 and (  # noqa: PLR2004
            next_dt - curr_dt
        ).total_seconds() <= 150:  # noqa: PLR2004
            avg = (prev_val + curr_val + next_val) / 3
            result.append((curr_dt, avg))
        else:
            result.append((curr_dt, curr_val))
    return result


def grouping_to_dict(
    lst: list[tuple[dt.datetime, float]],
) -> dict[str, list[str]]:
    """Convert raw list to dict of activities."""
    db: dict[str, list[str]] = {}

    lst2 = [(x[0], guess_activity(x[1])) for x in lst]
    del lst

    lst3: list[tuple[dt.datetime, str, int]] = []  # start, activity, duration

    current_activity = lst2[0][1]
    current_start = lst2[0][0]
    last_dt = current_start
    final_dt = lst2[-1][0]
    for this_dt, this_activity in lst2:
        dur = this_dt - current_start
        last_dt = this_dt
        if (
            this_activity == current_activity
            and this_dt != final_dt  # last row
            and this_dt - last_dt < dt.timedelta(minutes=5)  # missing data
        ):
            last_dt = this_dt
            continue
        # change of activity
        lst3.append((current_start, current_activity, round(dur.total_seconds() / 60)))
        current_activity = this_activity
        current_start = this_dt
        last_dt = this_dt
    del lst2

    for dt_start, activity, dur in lst3:
        # filter out idle short times
        # if dur < DURATION_MIN or activity in ("idle",):
        #     continue
        date = str(dt_start.date())
        time = f"{dt_start.strftime('%H:%M')}"
        s = f"{time} Media: {activity} ({dur} min)"
        append_data(db, date, s)

    return db


def main_influx(file_in: Path) -> dict[str, list[str]]:
    """Read influx-media.csv file and return dict."""
    lst = read_data_to_list(file_in)
    # lst = moving_average(lst)
    db = grouping_to_dict(lst)
    return db


if __name__ == "__main__":
    db = main_influx(FILE_IN)
    export_json(db=db, filename=FILE_IN.stem)
