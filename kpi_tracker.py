"""KPI tracking utilities for the lead harvester."""

from __future__ import annotations

import csv
import datetime as dt
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable
import argparse

PRD_PATH = Path(__file__).parent / "docs" / "PRD.md"
LOG_PATH = Path(__file__).parent / "data" / "kpi_log.csv"


@dataclass
class KPITargets:
    """KPI targets extracted from the PRD."""

    lead_quality_score: float | None = None
    response_rate: float | None = None
    close_rate: float | None = None
    daily_potential_revenue: float | None = None

    @classmethod
    def from_text(cls, text: str) -> "KPITargets":
        patterns = {
            "lead_quality_score": r"Lead quality score average ≥ (\d+(?:\.\d+)?)",
            "response_rate": r"Response rate ≥ (\d+)%",
            "close_rate": r"Close rate ≥ (\d+)%",
            "daily_potential_revenue": r"Daily potential revenue ≥ \$(\d+)",
        }
        kwargs: Dict[str, float] = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                kwargs[key] = float(match.group(1))
        return cls(**kwargs)


@dataclass
class RunMetrics:
    """Metrics for a single harvester run."""

    lead_quality_score: float
    response_rate: float
    close_rate: float
    daily_potential_revenue: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    @classmethod
    def from_cli(cls) -> "RunMetrics":
        parser = argparse.ArgumentParser(description="Log KPI metrics for a harvester run")
        parser.add_argument("--lead_quality_score", type=float, required=True)
        parser.add_argument("--response_rate", type=float, required=True)
        parser.add_argument("--close_rate", type=float, required=True)
        parser.add_argument("--daily_potential_revenue", type=float, required=True)
        args = parser.parse_args()
        return cls(
            lead_quality_score=args.lead_quality_score,
            response_rate=args.response_rate,
            close_rate=args.close_rate,
            daily_potential_revenue=args.daily_potential_revenue,
        )


class KPITracker:
    """Track KPI metrics and build dashboards."""

    def __init__(self, prd_path: Path = PRD_PATH, log_path: Path = LOG_PATH) -> None:
        self.prd_path = prd_path
        self.log_path = log_path
        self.log_path.parent.mkdir(exist_ok=True)
        text = self.prd_path.read_text(encoding="utf-8")
        self.targets = KPITargets.from_text(text)

    def log_run(self, metrics: RunMetrics) -> None:
        fieldnames = ["timestamp", *metrics.to_dict().keys()]
        exists = self.log_path.exists()
        with self.log_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not exists:
                writer.writeheader()
            row = {"timestamp": dt.datetime.now(dt.timezone.utc).isoformat(), **metrics.to_dict()}
            writer.writerow(row)

    def _average(self, rows: Iterable[dict]) -> Dict[str, float]:
        averages: Dict[str, float] = {}
        for key in rows[0].keys():
            if key == "timestamp":
                continue
            values = [float(r[key]) for r in rows if r.get(key)]
            averages[key] = sum(values) / len(values) if values else 0
        return averages

    def dashboard(self) -> str:
        if not self.log_path.exists():
            return "No KPI data logged yet."
        with self.log_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        averages = self._average(rows)
        lines = ["KPI Dashboard"]
        for key, avg in averages.items():
            target = getattr(self.targets, key)
            label = key.replace("_", " ").title()
            if target is not None:
                status = "✅" if avg >= target else "❌"
                lines.append(f"{label}: {avg:.2f} (target {target}) {status}")
            else:
                lines.append(f"{label}: {avg:.2f}")
        return "\n".join(lines)
