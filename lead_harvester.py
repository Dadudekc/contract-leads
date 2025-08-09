"""Main entrypoint for harvesting and processing leads."""

from __future__ import annotations

from pathlib import Path
import yaml

from scrapers import (
    CraigslistScraper,
    RedditScraper,
    RemoteOKScraper,
    WeWorkRemotelyScraper,
)
from scoring import LeadScorer
from outputs import export_all
from alerts import AlertSystem
from outreach import OutreachGenerator


def main() -> None:
    config = yaml.safe_load(Path("config.yaml").read_text())
    scrapers = [
        RemoteOKScraper(),
        CraigslistScraper(),
        RedditScraper(),
        WeWorkRemotelyScraper(),
    ]
    leads = []
    for scraper in scrapers:
        leads.extend(scraper.fetch())
    scorer = LeadScorer(config)
    scored = [scorer.score(lead) for lead in leads]
    scored.sort(key=lambda s: (s.score, s.lead.posted), reverse=True)
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    export_all(scored, output_dir)
    alert = AlertSystem(config)
    for s in scored:
        alert.maybe_alert(s)
    outreach = OutreachGenerator(config)
    for s in scored[:3]:
        outreach.generate(s)


if __name__ == "__main__":
    main()
