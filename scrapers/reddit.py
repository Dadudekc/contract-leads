"""Scraper for Reddit /r/forhire posts."""

from __future__ import annotations

import datetime as dt
from typing import List

import requests

from .base import Lead, Scraper

API_URL = "https://www.reddit.com/r/forhire/new.json?limit=10"


class RedditScraper(Scraper):
    """Fetch freelance leads from Reddit."""

    def fetch(self) -> List[Lead]:
        try:
            response = requests.get(API_URL, headers={"User-Agent": "contract-leads"}, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            return []
        leads: List[Lead] = []
        children = data.get("data", {}).get("children", [])
        for child in children:
            post = child.get("data", {})
            title = post.get("title", "")
            url = "https://www.reddit.com" + post.get("permalink", "")
            description = post.get("selftext", "")
            posted = dt.datetime.fromtimestamp(post.get("created_utc", 0), tz=dt.timezone.utc)
            leads.append(Lead(title=title, url=url, description=description, posted=posted))
        return leads
