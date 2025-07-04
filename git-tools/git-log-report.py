"""
Analyze git commits.

loop over all repositories
run git log to get commit head data and change stats
generate html report or all commits and week aggregate

this is a bit deprecated, better see
https://github.com/entorb/analyze-activities/blob/main/src/git_1_export_history.sh
https://github.com/entorb/analyze-activities/blob/main/src/git_2_analyze.py
"""  # noqa: INP001

import datetime as dt
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Literal

# from pprint import pprint
import pandas as pd


def run_git_log() -> str:
    """
    Run git log in cwd and return the result.

    filter: author=Torben
    """
    # git log --author="Torben" --date=iso-strict --pretty=format:'%cd<!!Split!!>%h<!!Split!!>%s<!!Split!!>%cn<!!Split!!>%an' --shortstat  # noqa: E501
    sp = subprocess.run(
        [  # noqa: S607
            "git",
            "log",
            "--author=Torben",
            "--date=iso-strict",
            # %cd: committer date
            # %h: abbreviated commit hash
            # %s: commit subject
            # %cn: committer name
            # %an: author name
            "--pretty=format:%ad<!!Split!!>%h<!!Split!!>%s<!!Split!!>%cn<!!Split!!>%an",
            "--shortstat",
        ],
        check=True,
        stdout=subprocess.PIPE,
    )
    res = sp.stdout.decode("utf-8")
    # 2024-01-23T23:10:23+01:00<!!Split!!>ea921be<!!Split!!>Added unit tests via pytest
    #  8 files changed, 523 insertions(+), 53 deletions(-)

    # 2023-10-05T11:33:48+02:00<!!Split!!>1365a19<!!Split!!>estimate: handling of H and M  # noqa: E501
    #  1 file changed, 12 insertions(+)
    return res


def extract_data_from_git_log(res: str) -> list[dict[str, Any]]:
    """Extract data from git log output."""
    if not res:
        msg = "git log response is empty"
        raise ValueError(msg)

    list_of_dict: list[dict[str, Any]] = []

    for element in res.split("\n\n"):  # split by empty line
        stats_dict: dict[str, Any] = {}

        # split item into header and stats by line break
        header, stats = element.split("\n ")

        # extract data from header
        # 2024-01-23T23:10:23+01:00<!!Split!!>ea83e18<!!Split!!>moved pre-commit to its own repo  # noqa: E501
        header_list = header.split("<!!Split!!>")
        # stats_dict["date"] = header_list[0]
        stats_dict["date"] = dt.datetime.fromisoformat(header_list[0]).replace(
            tzinfo=None
        )
        stats_dict["date"] = stats_dict["date"].replace(tzinfo=None)
        stats_dict["hash"] = header_list[1]
        stats_dict["title"] = header_list[2].replace("\t", " ")
        stats_dict["committer"] = header_list[3]
        stats_dict["author"] = header_list[4]

        # add week (start of week) of commit date
        year = stats_dict["date"].isocalendar()[0]
        week = stats_dict["date"].isocalendar()[1]
        stats_dict["week"] = dt.date.fromisocalendar(year, week, 1)
        del year, week

        # extract data from stats
        # 10 files changed, 12 insertions(+), 8 deletions(-)
        stats_list = stats.split(",")
        for x in stats_list:
            x = x.strip()  # noqa: PLW2901
            if "file" in x:
                y = re.sub(r" files? changed", "", x)
                stats_dict["files"] = int(y)
            elif "insertion" in x:
                y = re.sub(r" insertions?\(\+\)", "", x)
                stats_dict["insert"] = int(y)
            elif "deletion" in x:
                y = re.sub(r" deletions?\(\-\)", "", x)
                stats_dict["del"] = int(y)

        if "files" not in stats_dict:
            msg = "no files found in", element
            raise ValueError(msg)
        if "insert" not in stats_dict:
            stats_dict["insert"] = 0
        if "del" not in stats_dict:
            stats_dict["del"] = 0

        list_of_dict.append(stats_dict)

    # print(list_of_dict[0])
    return list_of_dict


def test_extract_data_from_git_log() -> None:  # noqa: D103
    res = """2024-01-28T22:30:59+01:00<!!Split!!>fbcc44c<!!Split!!>read-through ch 96<!!Split!!>Torben<!!Split!!>Torben
 1 file changed, 14 insertions(+), 23 deletions(-)

2024-01-25T19:22:52+01:00<!!Split!!>79881f1<!!Split!!>fix bad line endings<!!Split!!>Torben<!!Split!!>Torben
 3 files changed, 3 insertions(+)
"""  # noqa: E501
    data = extract_data_from_git_log(res)
    assert len(data) > 0
    assert data[0]["date"] == dt.datetime(2024, 1, 28, 22, 30, 59)  # noqa: DTZ001
    assert data[0]["hash"] == "fbcc44c"
    assert data[0]["title"] == "read-through ch 96"
    assert data[0]["files"] == 1
    assert data[0]["insert"] == 14  # noqa: PLR2004
    assert data[0]["del"] == 23  # noqa: PLR2004

    assert data[1]["files"] == 3  # noqa: PLR2004
    assert data[1]["insert"] == 3  # noqa: PLR2004
    assert data[1]["del"] == 0


test_extract_data_from_git_log()


def convert_data_to_df(data: list[dict[str, Any]]) -> pd.DataFrame:
    """
    Convert git data from dict to DataFrame.
    """
    df = pd.DataFrame.from_records(data)  # type: ignore
    df["insert"] = df["insert"].fillna(0).astype(int)  # type: ignore
    df["del"] = df["del"].fillna(0).astype(int)  # type: ignore

    # add column of time
    df["time"] = df["date"].dt.time
    df["hour"] = df["date"].dt.hour

    # add column of shift 6:00, 14:00, 22:00
    df["shift"] = df["date"].dt.hour.apply(_get_shift)  # type: ignore

    df["days_ago"] = (dt.datetime.today() - df["date"]).dt.days  # type: ignore  # noqa: DTZ002
    return df


# Calculate the shifts based on the hour
def _get_shift(hour: int) -> Literal["morning", "afternoon", "night"]:
    if 6 <= hour < 14:  # noqa: PLR2004
        return "morning"
    elif 14 <= hour < 22:  # noqa: PLR2004, RET505
        return "afternoon"
    else:
        return "night"


if __name__ == "__main__":
    # res = run_git_log()
    # commit_head_data = extract_data_from_git_log(res)
    # print(commit_head_data)
    # exit()

    # if run in a repo, go to parent dir
    p = Path()  # cwd
    if (p / ".git").is_dir():
        os.chdir("..")

    # loop over all dirs, add the git repos to list
    p = Path()
    list_of_repos = sorted(
        [x for x in p.iterdir() if x.is_dir() and (x / ".git").is_dir()]
    )

    df_all = pd.DataFrame()

    for d in list_of_repos:
        print(d)
        os.chdir(d)
        res = run_git_log()
        data = extract_data_from_git_log(res)
        assert len(data) > 0, f"no git commit data in {d}"
        # pprint(data[-1])
        df = convert_data_to_df(data)
        # add column of dir name
        df["repo"] = d.name
        # append to df_all
        df_all = pd.concat([df_all, df], ignore_index=True)
        os.chdir("..")
        # break

    df_all = df_all.sort_values(by=["date"], ascending=False)  # type: ignore
    # html export
    df_all[
        [
            "date",
            "repo",
            "hash",
            "title",
            "committer",
            "author",
            "files",
            "insert",
            "del",
        ]
    ].to_html("git-log-report-all.html", index=False, justify="center")  # type: ignore

    # filter on date <= 30 days from today
    df_all["date"]

    # week report
    df = df_all.groupby(["week", "repo"]).agg(  # type: ignore
        commits=("date", "count"),
        files=("files", "sum"),
        inserts=("insert", "sum"),
        dels=("del", "sum"),
    )
    # sort by index week desc and repos asc
    df = df.sort_values(by=["week", "repo"], ascending=[False, True])  # type: ignore
    # export
    df.to_html("git-log-report-weekly.html", index=True, justify="center")  # type: ignore

    # filter on last 30 days
    df30d = df_all.query("days_ago <= 30")
    # group by hour
    df = df30d.groupby(["hour"]).agg(commits=("date", "count"))  # type: ignore
    print(df)
    # group by shift
    df = df30d.groupby(["shift"]).agg(commits=("date", "count"))  # type: ignore
    print(df)
