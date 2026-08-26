"""Simple Minimal App."""

from pathlib import Path

import streamlit as st

from helper import get_photos_db

st.set_page_config(page_title="Mac Photos Report ", page_icon=None, layout="wide")


def create_navigation_menu() -> None:
    """Create and populate navigation menu."""
    lst = []
    for p in sorted(Path("src/reports").glob("*.py")):
        f = p.stem
        t = f[4:].title()
        lst.append(st.Page(page=f"reports/{f}.py", title=t))
    pg = st.navigation(lst)
    pg.run()


create_navigation_menu()
db = get_photos_db()
