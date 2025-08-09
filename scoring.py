"""Lead scoring engine."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Dict, List

from scrapers import Lead


@dataclass
class ScoredLead:
    """Lead with an associated score."""

    lead: Lead
    score: float


class LeadScorer:
    """Score leads based on simple keyword and recency heuristics."""

    def __init__(self, config: Dict):
        self.keywords = [k.lower() for k in config.get("keywords", [])]
        self.weights = config.get("scoring", {})

    def score(self, lead: Lead) -> ScoredLead:
        text = f"{lead.title} {lead.description}".lower()
        keyword_hits = sum(text.count(k) for k in self.keywords)
        keyword_score = keyword_hits * self.weights.get("keyword_weight", 1.0)
        days_old = (dt.datetime.now(dt.timezone.utc) - lead.posted).days
        recency_score = max(0.0, self.weights.get("recency_weight", 0.5) * (30 - days_old))
        return ScoredLead(lead=lead, score=keyword_score + recency_score)
