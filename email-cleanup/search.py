"""Search for cleanup candidates in my email inbox."""

import csv
import email
import imaplib
import re
import tomllib
from collections import Counter
from dataclasses import dataclass, field
from email.header import decode_header
from email.utils import parseaddr
from pathlib import Path

IMAP_CREDS = Path("creds-uberspace.toml")
IMAP_FOLDER = "INBOX"

# IMAP_CREDS = Path("creds-web.toml")
# IMAP_FOLDER = "Unbekannt"  # "INBOX", "Unbekannt"


# --- config ---
FETCH_LAST_N = 1_000
TOP_N = 50
CSV_DIR = Path("out")
CSV_DIR.mkdir(exist_ok=True)


# --- data ---
@dataclass
class MailStats:
    """Collected lists of senders, domains, and normalized subjects."""

    senders: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    subjects: list[str] = field(default_factory=list)


# --- helpers ---
def list_folders(conn: imaplib.IMAP4_SSL) -> None:
    """Print all top-level IMAP folders of the account."""
    title = "Folders"
    print(f"\n{'=' * 40}\n{title}\n{'=' * 40}")
    _, folders = conn.list()
    for folder in folders:
        if not isinstance(folder, bytes):
            continue
        # format: (\Flags) "delimiter" "name"
        parts = folder.decode().split('"')
        name = parts[-1].strip()
        print(name)


def decode_subject(raw: str) -> str:
    """Decode RFC 2047 encoded subject header to a plain Unicode string."""
    parts = decode_header(raw)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded.append(
                part.decode(charset or "utf-8", errors="replace")
                if charset and charset.lower() != "unknown-8bit"
                else part.decode("latin-1", errors="replace")
            )
        else:
            decoded.append(part)
    return "".join(decoded)


def normalize_subject(raw: str) -> str:
    """
    Decode subject.

    use leading [tag] as key if present, else collapse numbers and truncate to 5 words.
    """
    # [topic] ...
    subj = decode_subject(raw)
    if m := re.match(r"(\[[^\]]+\])", subj):
        return m.group(1).lower()
    subj = subj.lower().strip()

    subj = re.sub(r"^(?:(?:re|aw|fwd): )+", "", subj)  # leading re:/aw:

    subj = re.sub(r"\d+", "N", subj)  # collapse all numbers to N
    subj = " ".join(subj.split()[:5])  # first 5 words only
    return subj.strip()


def fetch_stats(conn: imaplib.IMAP4_SSL) -> MailStats:
    """Fetch From and Subject for the last N emails -> parsed stats."""
    conn.select(IMAP_FOLDER)
    _, id_data = conn.search(None, "ALL")
    ids = id_data[0].split()[-FETCH_LAST_N:]

    stats = MailStats()
    for uid in ids:
        # BODY.PEEK does not mark emails as read
        _, raw = conn.fetch(uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
        if not raw or raw[0] is None:
            continue
        raw_bytes = raw[0][1]
        if not isinstance(raw_bytes, bytes):
            continue
        msg = email.message_from_bytes(raw_bytes)

        _name, email_addr = parseaddr(msg.get("From", ""))
        email_addr = email_addr.lower()
        stats.senders.append(email_addr)

        if "@" in email_addr:
            stats.domains.append(email_addr.split("@")[1])

        stats.subjects.append(normalize_subject(msg.get("Subject", "")))

    return stats


def print_ranking(title: str, counts: Counter[str], top_n: int = TOP_N) -> None:
    """Print the top_n entries of a Counter as a formatted ranking to stdout."""
    print(f"\n{'=' * 40}\n{title}\n{'=' * 40}")
    for value, count in counts.most_common(top_n):
        if count == 1:
            break
        print(f"{count:4d}  {value}")


def export_csv(
    directory: Path, category: str, counts: Counter[str], top_n: int = TOP_N
) -> None:
    """Write the top N entries of Counter to .csv in directory."""
    path = directory / f"{category}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["value", "count"])
        for value, count in counts.most_common(top_n):
            writer.writerow([value, count])
    print(f"CSV written to {path}")


# --- main ---
def main() -> None:
    """Load credentials, fetch inbox stats, print rankings, and export CSVs."""
    with IMAP_CREDS.open("rb") as f:
        creds = tomllib.load(f)

    with imaplib.IMAP4_SSL(creds["IMAP_HOST"]) as conn:
        conn.login(creds["IMAP_USER"], creds["IMAP_PASS"])
        list_folders(conn)
        stats = fetch_stats(conn)

    rankings = {
        "sender": Counter(stats.senders),
        "domain": Counter(stats.domains),
        "subject": Counter(stats.subjects),
    }

    for title, counts in rankings.items():
        print_ranking(f"Top {TOP_N} {title}s", counts)
        export_csv(CSV_DIR, title, counts)


if __name__ == "__main__":
    main()

# cspell:ignore Unbekannt
