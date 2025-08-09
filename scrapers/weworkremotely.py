"""Scraper for WeWorkRemotely listings."""

from __future__ import annotations

import datetime as dt
import email.utils as eut
import xml.etree.ElementTree as ET
from typing import List

import requests

from .base import Lead, Scraper

RSS_URL = "https://weworkremotely.com/categories/remote-programming-jobs.rss"


class WeWorkRemotelyScraper(Scraper):
    """Fetch freelance leads from WeWorkRemotely RSS feed."""

    def fetch(self) -> List[Lead]:
        try:
            response = requests.get(RSS_URL, headers={"User-Agent": "contract-leads"}, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.content)
        except requests.RequestException:
            return []
        leads: List[Lead] = []
        for item in root.findall(".//item"):
            title = item.findtext("title", default="")
            url = item.findtext("link", default="")
            description = item.findtext("description", default="")
            pubdate = item.findtext("pubDate")
            try:
                posted = eut.parsedate_to_datetime(pubdate) if pubdate else dt.datetime.now(dt.timezone.utc)
            except (TypeError, ValueError):
                posted = dt.datetime.now(dt.timezone.utc)
            leads.append(Lead(title=title, url=url, description=description, posted=posted))
        return leads
