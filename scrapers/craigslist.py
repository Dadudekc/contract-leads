"""Placeholder scraper for Craigslist."""

from __future__ import annotations

from typing import List

from .base import Lead, Scraper


class CraigslistScraper(Scraper):
    """Scrape freelance leads from Craigslist."""

    def fetch(self) -> List[Lead]:
        # TODO: implement Craigslist scraping
        return []
