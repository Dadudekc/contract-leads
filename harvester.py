"""CLI entrypoint for the lead harvester KPI tracker."""

from __future__ import annotations

from kpi_tracker import KPITracker, RunMetrics


class HarvesterApp:
    """Coordinate KPI tracking operations."""

    def __init__(self, tracker: KPITracker | None = None) -> None:
        self.tracker = tracker or KPITracker()

    def execute(self, metrics: RunMetrics) -> str:
        self.tracker.log_run(metrics)
        return self.tracker.dashboard()


def main() -> None:
    metrics = RunMetrics.from_cli()
    app = HarvesterApp()
    print(app.execute(metrics))


if __name__ == "__main__":
    main()
