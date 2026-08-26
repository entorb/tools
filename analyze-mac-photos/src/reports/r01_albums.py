"""Albums."""

import pandas as pd
import streamlit as st

from helper import get_db_size, get_logger_from_filename, get_photos_db

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore


@st.cache_data(ttl="2h")
def get_folders() -> list[str]:
    """
    Return list of all folder names.

    via loop over albums
    """
    db = get_photos_db()
    folders = {a.parent.title for a in db.album_info if a.parent}
    return sorted(folders)


@st.cache_data(ttl="2h")
def get_albums(
    folders_in: list[str] | None, folders_ex: list[str] | None
) -> pd.DataFrame:
    """Return DataFrame of albums."""
    db = get_photos_db()
    db_photo_cnt, db_size_mb = get_db_size()
    data = []
    for a in db.album_info:
        # skip folder filter is set and matching
        parent = a.parent.title if a.parent else ""
        if folders_in and parent not in folders_in:
            continue
        if folders_ex and parent in folders_ex:
            continue
        cnt_photos = len(a.photos)
        size = int(round(sum(p.original_filesize for p in a.photos) / 1048576, 0))
        data.append(
            (
                a.title,
                parent,
                cnt_photos,
                round(100 * cnt_photos / db_photo_cnt, 1),
                size,
                round(100 * size / db_size_mb, 1),
            )
        )

    df = pd.DataFrame(data, columns=("Name", "Parent", "Count", "Count%", "MB", "MB%"))
    return df.sort_values("MB", ascending=False)


col1, col2 = st.columns((1, 1))
sel_folders_in = col1.multiselect(label="Folder Include", options=get_folders())
sel_folders_ex = col2.multiselect(label="Folder Exclude", options=get_folders())

df = get_albums(folders_in=sel_folders_in, folders_ex=sel_folders_ex)
db_photo_cnt, db_size_mb = get_db_size()
st.dataframe(
    df,
    hide_index=True,
    width="stretch",
    column_config={
        "Count": st.column_config.ProgressColumn(
            format="%d", max_value=int(df["Count"].max())
        ),
        "Count%": st.column_config.NumberColumn(format="%.1f", width="small"),
        "MB": st.column_config.ProgressColumn(
            format="%d", max_value=int(df["MB"].max())
        ),
        "MB%": st.column_config.NumberColumn(format="%.1f", width="small"),
    },
)
