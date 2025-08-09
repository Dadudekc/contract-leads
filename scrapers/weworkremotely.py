"""Placeholder scraper for WeWorkRemotely."""

from __future__ import annotations

from typing import List

from .base import Lead, Scraper


class WeWorkRemotelyScraper(Scraper):
    """Scrape freelance leads from WeWorkRemotely."""

    def fetch(self) -> List[Lead]:
        # TODO: implement WeWorkRemotely scraping
        return []
