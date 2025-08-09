"""Scraper for RemoteOK job listings."""

from __future__ import annotations

import datetime as dt
from typing import List

import requests

from .base import Lead, Scraper

API_URL = "https://remoteok.com/api"


class RemoteOKScraper(Scraper):
    """Fetch leads from the RemoteOK API."""

    def fetch(self) -> List[Lead]:
        try:
            response = requests.get(API_URL, headers={"User-Agent": "contract-leads"}, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            return []
        leads: List[Lead] = []
        for item in data:
            if not isinstance(item, dict) or "position" not in item:
                continue
            posted = dt.datetime.fromtimestamp(item.get("epoch", 0), tz=dt.timezone.utc)
            leads.append(
                Lead(
                    title=item.get("position", ""),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    posted=posted,
                )
            )
        return leads
