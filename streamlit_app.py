from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

APP_NAME = "Jadel Pages API"
APP_DOMAIN = "jadelapp-meta.streamlit.app"
CONTACT_EMAIL = "darklife_jade@hotmail.com"
BASE_URL = f"https://{APP_DOMAIN}"
EFFECTIVE_DATE = date(2026, 7, 18)

VALID_VIEWS = {
    "home",
    "privacy",
    "terms",
    "data-deletion",
}


def get_view() -> str:
    """Return a supported public page from the