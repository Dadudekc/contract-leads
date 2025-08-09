"""KPI dashboard utilities."""

from __future__ import annotations

from typing import Dict
import sqlite3

from .tracker import KPITracker

PRD_TARGETS = {
    "avg_quality": 10.0,
    "response_rate": 30.0,
    "close_rate": 10.0,
    "daily_revenue": 300.0,
}


class KPIDashboard:
    """Render aggregate KPI information and compare with PRD targets."""

    def __init__(self, tracker: KPITracker) -> None:
        self.tracker = tracker

    def snapshot(self) -> Dict[str, float]:
        """Return current metrics including derived daily revenue."""

        data = self.tracker.aggregate()
        with sqlite3.connect(self.tracker.db_path) as conn:
            cur = conn.execute("SELECT COUNT(*) FROM runs")
            run_count = cur.fetchone()[0] or 0
        daily_revenue = (data["revenue"] / run_count) if run_count else 0.0
        data["daily_revenue"] = daily_revenue
        return data

    def render(self) -> str:
        """Return a human-readable dashboard string."""

        data = self.snapshot()
        lines = ["# KPI Dashboard"]
        for key, target in PRD_TARGETS.items():
            current = data.get(key, 0.0)
            status = "✅" if current >= target else "⚠️"
            lines.append(
                f"- {key.replace('_', ' ').title()}: {current:.2f} (target {target}) {status}"
            )
        return "\n".join(lines)

