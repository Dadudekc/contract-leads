"""Outreach message generation utilities."""

from __future__ import annotations

from typing import Dict

from scoring import ScoredLead


class OutreachGenerator:
    """Generate simple outreach messages for leads."""

    def __init__(self, config: Dict):
        self.pricing = config.get("pricing", {})

    def suggest_price(self, lead: ScoredLead) -> float:
        base = self.pricing.get("base", 1000)
        return float(base)

    def generate(self, lead: ScoredLead, tone: str = "friendly") -> str:
        price = self.suggest_price(lead)
        templates = {
            "friendly": "Hi there, I saw your post about {title}. I'd love to help!",
            "formal": "Hello, I am reaching out regarding {title}.",
        }
        template = templates.get(tone, templates["friendly"])
        return f"{template.format(title=lead.lead.title)}\nEstimated price: ${price:,.0f}\n{lead.lead.url}"
