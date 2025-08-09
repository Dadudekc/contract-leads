"""Core harvester runner."""

from __future__ import annotations

from .tracker import KPITracker, KPIMetrics


class LeadHarvester:
    """Main entry point for harvesting runs."""

    def __init__(self, tracker: KPITracker | None = None) -> None:
        self.tracker = tracker or KPITracker()

    def run(self, metrics: KPIMetrics) -> None:
        """Record metrics for a harvesting session.

        A real implementation would gather leads before logging results.
        """

        self.tracker.log_run(metrics)

