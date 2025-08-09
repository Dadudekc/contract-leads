"""Lead scoring engine."""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from typing import Dict, List

from scrapers import Lead


@dataclass
class ScoredLead:
    """Lead with an associated score."""

    lead: Lead
    score: float


class LeadScorer:
    """Score leads using keyword and heuristic signals."""

    def __init__(self, config: Dict):
        self.keywords = [k.lower() for k in config.get("keywords", [])]
        self.weights = config.get("scoring", {})
        budget = config.get("budget", {})
        self.budget_min = budget.get("min", 0)
        self.budget_max = budget.get("max", 0)
        self.urgency_words = ["asap", "urgent", "immediately", "today"]
        self.decision_phrases = [
            "my business",
            "my store",
            "i need",
            "we need",
            "i'm looking",
        ]

    def score(self, lead: Lead) -> ScoredLead:
        text = f"{lead.title} {lead.description}".lower()
        score = 0.0

        keyword_hits = sum(text.count(k) for k in self.keywords)
        score += keyword_hits * self.weights.get("keyword_weight", 1.0)

        days_old = (dt.datetime.now(dt.timezone.utc) - lead.posted).days
        score += max(0.0, self.weights.get("recency_weight", 0.5) * (30 - days_old))

        if any(w in text for w in self.urgency_words):
            score += self.weights.get("urgency_weight", 0.0)

        for match in re.findall(r"\$([0-9,]+)", text):
            value = float(match.replace(",", ""))
            if self.budget_min <= value <= self.budget_max:
                score += self.weights.get("budget_weight", 0.0)
                break

        if any(p in text for p in self.decision_phrases):
            score += self.weights.get("decision_maker_weight", 0.0)

        word_count = len(lead.description.split())
        if word_count <= 50:
            score += self.weights.get("dm_friendliness_weight", 0.0)

        return ScoredLead(lead=lead, score=score)
