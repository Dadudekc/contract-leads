"""KPI tracking utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import sqlite3
from typing import Dict


@dataclass
class KPIMetrics:
    """Data collected for a single harvester run."""

    leads_found: int
    leads_contacted: int
    leads_closed: int
    revenue: float
    avg_quality: float = 0.0
    run_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class KPITracker:
    """Persist and aggregate KPI metrics."""

    def __init__(self, db_path: str = "kpi_metrics.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_at TEXT PRIMARY KEY,
                    leads_found INTEGER,
                    leads_contacted INTEGER,
                    leads_closed INTEGER,
                    revenue REAL,
                    avg_quality REAL
                )
                """
            )
            conn.commit()

    def log_run(self, metrics: KPIMetrics) -> None:
        """Store metrics for a single run."""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO runs (
                    run_at,
                    leads_found,
                    leads_contacted,
                    leads_closed,
                    revenue,
                    avg_quality
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    metrics.run_at.isoformat(),
                    metrics.leads_found,
                    metrics.leads_contacted,
                    metrics.leads_closed,
                    metrics.revenue,
                    metrics.avg_quality,
                ),
            )
            conn.commit()

    def aggregate(self) -> Dict[str, float]:
        """Return aggregate statistics across all runs."""

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT SUM(leads_found), SUM(leads_contacted), SUM(leads_closed), SUM(revenue), SUM(avg_quality * leads_found) FROM runs"
            )
            row = cur.fetchone()

        leads_found, leads_contacted, leads_closed, revenue, quality_sum = [r or 0 for r in row]
        response_rate = (leads_contacted / leads_found * 100) if leads_found else 0.0
        close_rate = (leads_closed / leads_contacted * 100) if leads_contacted else 0.0
        avg_quality = (quality_sum / leads_found) if leads_found else 0.0
        return {
            "leads_found": leads_found,
            "leads_contacted": leads_contacted,
            "leads_closed": leads_closed,
            "revenue": revenue,
            "avg_quality": avg_quality,
            "response_rate": response_rate,
            "close_rate": close_rate,
        }

