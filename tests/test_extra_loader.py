"""Tests for dynamic loading of extra scrapers."""

from __future__ import annotations

import datetime as dt
import importlib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from extra_sources.loader import load_extra_scrapers


def test_load_extra_scrapers_discovers_custom_scrapers() -> None:
    pkg_path = Path(__file__).resolve().parents[1] / "extra_sources"
    mod_path = pkg_path / "dummy_source.py"
    mod_path.write_text(
        "from scrapers.base import Scraper, Lead\n"
        "import datetime as dt\n"
        "class DummyScraper(Scraper):\n"
        "    def fetch(self):\n"
        "        return [Lead(title='d', url='u', description='x', posted=dt.datetime.now(dt.timezone.utc))]\n"
    )
    try:
        importlib.invalidate_caches()
        scrapers = load_extra_scrapers()
        assert any(s.__class__.__name__ == "DummyScraper" for s in scrapers)
    finally:
        mod_path.unlink()
        importlib.invalidate_caches()
