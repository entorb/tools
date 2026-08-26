"""Fix names and abbreviations."""

import re


def name_fix(title: str) -> str:
    """Fix names and abbreviations."""
    # cspell: disable
    title = re.sub(r"\bGeb\.?\b", "Geburtstag", title)
    # cspell: enable
    return title
