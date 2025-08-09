"""Placeholder scraper for Reddit."""

from __future__ import annotations

from typing import List

from .base import Lead, Scraper


class RedditScraper(Scraper):
    """Scrape freelance leads from Reddit."""

    def fetch(self) -> List[Lead]:
        # TODO: implement Reddit scraping
        return []
