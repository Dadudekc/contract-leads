"""Tests for the lead scoring engine."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scrapers.base import Lead
from scoring import LeadScorer


def make_lead(text: str) -> Lead:
    return Lead(
        title="t",
        url="u",
        description=text,
        posted=dt.datetime.now(dt.timezone.utc),
    )


def test_scoring_combines_multiple_factors() -> None:
    config = {
        "keywords": ["python"],
        "budget": {"min": 50, "max": 500},
        "scoring": {
            "keyword_weight": 1.0,
            "recency_weight": 0.0,
            "urgency_weight": 2.0,
            "budget_weight": 1.5,
            "decision_maker_weight": 1.0,
            "dm_friendliness_weight": 1.0,
        },
    }
    text = "Need Python script ASAP for my business, budget $200."
    score = LeadScorer(config).score(make_lead(text)).score
    expected = 1.0 + 2.0 + 1.5 + 1.0 + 1.0
    assert score == pytest.approx(expected)


def test_budget_out_of_range_not_scored() -> None:
    config = {
        "keywords": [],
        "budget": {"min": 50, "max": 500},
        "scoring": {
            "keyword_weight": 0.0,
            "recency_weight": 0.0,
            "budget_weight": 1.0,
        },
    }
    in_range = "Budget $200 available"
    out_range = "Budget $1000 available"
    scorer = LeadScorer(config)
    assert scorer.score(make_lead(in_range)).score == pytest.approx(1.0)
    assert scorer.score(make_lead(out_range)).score == 0.0
