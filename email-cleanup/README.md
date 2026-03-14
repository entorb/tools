# Email Cleanup Candidates

Scan your IMAP inbox to rank senders, domains, and subjects to identify candidates as input for email cleanup filters.

## Setup

Provide your credentials in `creds.toml` based on `creds.EXAMPLE.toml`.

## Usage

```bash
python search.py
```

Output CSVs are written to the `out/` directory:

| File | Contents |
| --- | --- |
| `sender.csv` | Top senders by email address |
| `domain.csv` | Top sender domains |
| `subject.csv` | Top subjects (after cleanup) |

## Inbox cleanup

using this output you can then

1. unsubscribe newsletters
2. create filters for automatic deletion of irrelevant emails
3. use "Smart Mailboxes" to manually delete irrelevant emails

## General Tips

Use a secondary email address for newsletter and online shopping.
