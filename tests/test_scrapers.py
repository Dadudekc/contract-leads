"""Tests for scraper implementations."""

from __future__ import annotations

from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scrapers.craigslist import CraigslistScraper
from scrapers.reddit import RedditScraper
from scrapers.weworkremotely import WeWorkRemotelyScraper


def make_response(*, text: str | None = None, json_data: dict | None = None) -> Mock:
    response = Mock()
    response.raise_for_status.return_value = None
    if text is not None:
        response.content = text.encode("utf-8")
    if json_data is not None:
        response.json.return_value = json_data
    else:
        response.json.return_value = {}
    return response


def test_weworkremotely_fetch() -> None:
    rss = (
        "<rss><channel><item><title>Job</title><link>http://ex.com</link>"
        "<description>desc</description><pubDate>Wed, 01 Jan 2020 00:00:00 +0000"\
        "</pubDate></item></channel></rss>"
    )
    with patch("requests.get", return_value=make_response(text=rss)):
        leads = WeWorkRemotelyScraper().fetch()
    assert len(leads) == 1
    assert leads[0].title == "Job"
    assert leads[0].url == "http://ex.com"


def test_craigslist_fetch() -> None:
    rss = (
        "<rss><channel><item><title>CL Job</title><link>http://cl.com</link>"
        "<description>desc</description><pubDate>Wed, 01 Jan 2020 00:00:00 +0000"\
        "</pubDate></item></channel></rss>"
    )
    with patch("requests.get", return_value=make_response(text=rss)):
        leads = CraigslistScraper().fetch()
    assert len(leads) == 1
    assert leads[0].url == "http://cl.com"


def test_reddit_fetch() -> None:
    data = {
        "data": {
            "children": [
                {
                    "data": {
                        "title": "Reddit Job",
                        "permalink": "/r/test",
                        "selftext": "desc",
                        "created_utc": 1609459200,
                    }
                }
            ]
        }
    }
    with patch("requests.get", return_value=make_response(json_data=data)):
        leads = RedditScraper().fetch()
    assert len(leads) == 1
    assert leads[0].title == "Reddit Job"
