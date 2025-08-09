"""Example entry point for the lead harvester."""

from __future__ import annotations

import argparse

from lead_harvester import KPITracker, KPIMetrics, LeadHarvester, KPIDashboard


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log a harvester run and display KPIs")
    parser.add_argument("--found", type=int, default=0, help="leads found this run")
    parser.add_argument("--contacted", type=int, default=0, help="leads contacted")
    parser.add_argument("--closed", type=int, default=0, help="leads closed")
    parser.add_argument("--revenue", type=float, default=0.0, help="revenue earned")
    parser.add_argument("--quality", type=float, default=0.0, help="average quality score")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    tracker = KPITracker()
    harvester = LeadHarvester(tracker)
    metrics = KPIMetrics(
        leads_found=args.found,
        leads_contacted=args.contacted,
        leads_closed=args.closed,
        revenue=args.revenue,
        avg_quality=args.quality,
    )
    harvester.run(metrics)
    dashboard = KPIDashboard(tracker)
    print(dashboard.render())


if __name__ == "__main__":  # pragma: no cover
    main()

