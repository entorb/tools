"""Photos."""

import osxphotos
import pandas as pd
import streamlit as st
from bitmath import MiB

from helper import (
    date_from_weeks,
    get_logger_from_filename,
    get_photos_db,
)

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore

TABLE_FORMAT_DATETIME = st.column_config.DateColumn(format="DD.MM.YYYY HH:mm")
TABLE_FORMAT_DATE = st.column_config.DateColumn(format="DD.MM.YYYY")


def photo_query_res_to_df(res: list[osxphotos.PhotoInfo]) -> pd.DataFrame:
    """Convert a list of PhotoInfo objects to a pandas DataFrame."""
    data = [
        (
            p.original_filename,
            p.date.replace(tzinfo=None),
            round(p.original_filesize / 1048576, 1),
            p.path,
        )
        for p in res
    ]
    df = pd.DataFrame(data, columns=("Filename", "Date", "MB", "Path"))
    df["Date"] = pd.to_datetime(df["Date"])
    return df


@st.cache_data(ttl="2h")
def get_photos_no_album(weeks: int) -> pd.DataFrame:  # osxphotos.PhotoInfo
    """Get photos without album."""
    from_date = date_from_weeks(weeks)
    res = db.query(
        osxphotos.QueryOptions(not_in_album=True, from_date=from_date, not_hidden=True)
    )
    return photo_query_res_to_df(res).sort_values("Date", ascending=False)


@st.cache_data(ttl="2h")
def get_photos_large(weeks: int, mb: int) -> pd.DataFrame:  # osxphotos.PhotoInfo
    """Get large photos."""
    from_date = date_from_weeks(weeks)
    min_size = MiB(mb)
    res = db.query(osxphotos.QueryOptions(min_size=min_size, from_date=from_date))
    return photo_query_res_to_df(res).sort_values("MB", ascending=False)


db = get_photos_db()

col1, col2 = st.columns((1, 5))
# 0 results in no filter
weeks = col1.number_input(label="Weeks", min_value=0, value=8, step=4)
st.columns(1)

st.header("Photos without Album")
df = get_photos_no_album(weeks=weeks)
st.dataframe(
    df,
    hide_index=True,
    width="stretch",
    column_config={
        "Date": TABLE_FORMAT_DATETIME,
        "MB": st.column_config.NumberColumn(format="%.1f"),
    },
)

st.header("Days with many unsorted Photos")
df["Date"] = df["Date"].dt.date
df = df[["Date"]].groupby("Date").agg(count=("Date", "count")).query("count >= 10")
df = df.reset_index().sort_values("Date", ascending=False)
st.dataframe(
    df,
    hide_index=True,
    width="content",
    column_config={"Date": TABLE_FORMAT_DATE},
)

st.header("Large Files")
df = get_photos_large(weeks=weeks, mb=50)
st.dataframe(
    df,
    hide_index=True,
    width="stretch",
    column_config={
        "Date": TABLE_FORMAT_DATETIME,
        "MB": st.column_config.ProgressColumn(
            format="%d", max_value=int(df["MB"].max()) if not df.empty else 0
        ),
    },
)
