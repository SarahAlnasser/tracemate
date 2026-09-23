"""
Talks to the backend (see docs/api.md).

Week 6: fetch_session() and upload_attempt().
Week 7: if upload fails (no Wi-Fi), save to data/queue/ and retry with sync_queue().
"""
import requests

import config


def fetch_session():
    """GET the next session for this device. Returns a dict, or None if offline."""
    raise NotImplementedError("Week 6")


def upload_attempt(attempt):
    """POST one attempt. On failure, add it to the offline queue."""
    raise NotImplementedError("Week 6")


def sync_queue():
    """Send every queued attempt, oldest first."""
    raise NotImplementedError("Week 7")
