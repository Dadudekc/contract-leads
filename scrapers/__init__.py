"""Scraper package for harvesting leads from various sources."""

from .base import Lead, Scraper
from .remoteok import RemoteOKScraper
from .craigslist import CraigslistScraper
from .reddit import RedditScraper
from .weworkremotely import WeWorkRemotelyScraper

__all__ = [
    "Lead",
    "Scraper",
    "RemoteOKScraper",
    "CraigslistScraper",
    "RedditScraper",
    "WeWorkRemotelyScraper",
]
