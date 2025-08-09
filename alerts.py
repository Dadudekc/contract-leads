"""Alerting system for high-value leads."""

from __future__ import annotations

from typing import Dict

import requests

from scoring import ScoredLead


class AlertSystem:
    """Send Telegram alerts when lead scores exceed a threshold."""

    def __init__(self, config: Dict):
        telegram = config.get("telegram", {})
        self.enabled = telegram.get("enabled", False)
        self.token = telegram.get("bot_token")
        self.chat_id = telegram.get("chat_id")
        self.threshold = config.get("alerts", {}).get("min_score", 0)

    def maybe_alert(self, lead: ScoredLead) -> None:
        if not self.enabled or lead.score < self.threshold:
            return
        message = f"Lead: {lead.lead.title} ({lead.score:.2f})\n{lead.lead.url}"
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        requests.post(url, data={"chat_id": self.chat_id, "text": message}, timeout=30)
