"""Helper functions."""

import datetime as dt
from pathlib import Path
from typing import TYPE_CHECKING

import osxphotos
import streamlit as st
from streamlit.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger


def get_logger_from_filename(file: str) -> Logger:
    """Return logger using filename name."""
    return get_logger(Path(file).stem)


@st.cache_resource
def get_photos_db() -> osxphotos.PhotosDB:
    """Get cached photos DB resource."""
    return osxphotos.PhotosDB()


def date_from_weeks(weeks: int) -> dt.datetime | None:
    """Return datetime: now-weeks."""
    if weeks > 0:
        return dt.datetime.now(tz=dt.UTC) - dt.timedelta(weeks=weeks)
    return None


@st.cache_data
def get_db_size() -> tuple[int, int]:
    """Return total count of items and MB."""
    size = 0
    db = get_photos_db()
    cnt = len(db.photos())
    for p in db.photos():
        size += p.original_filesize
    return cnt, int(size / (1024 * 1024))
