"""Join the single files."""

import datetime as dt
import json
from pathlib import Path

from helper import export_json

MIN_DATE = dt.date(2025, 1, 1)


def main() -> None:  # noqa: D103
    db: dict[str, list[str]] = {}

    for source in ("cal", "git", "strava", "oura", "lifelog", "rtm"):
        p = Path(f"output/{source}.json")
        print(source)
        with p.open(encoding="utf-8") as fh:
            d_json = json.load(fh)

        for datestr, lst in d_json.items():
            date = dt.date.fromisoformat(datestr)
            if date < MIN_DATE:
                continue
            if datestr in db:
                db[datestr].extend(lst)
            else:
                db[datestr] = lst

    export_json(db, "join")


if __name__ == "__main__":
    main()
