"""Output utilities for scored leads."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from scoring import ScoredLead


def export_csv(leads: Iterable[ScoredLead], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url", "score", "posted", "description"])
        for s in leads:
            writer.writerow([s.lead.title, s.lead.url, f"{s.score:.2f}", s.lead.posted.isoformat(), s.lead.description])


def export_markdown(leads: Iterable[ScoredLead], path: Path) -> None:
    lines = ["| Title | Score | Posted |", "| --- | ---: | --- |"]
    for s in leads:
        lines.append(f"| [{s.lead.title}]({s.lead.url}) | {s.score:.2f} | {s.lead.posted.date()} |")
    path.write_text("\n".join(lines), encoding="utf-8")


def export_json(leads: Iterable[ScoredLead], path: Path) -> None:
    data = [
        {
            "title": s.lead.title,
            "url": s.lead.url,
            "score": s.score,
            "posted": s.lead.posted.isoformat(),
            "description": s.lead.description,
        }
        for s in leads
    ]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def export_all(leads: Iterable[ScoredLead], directory: Path) -> None:
    export_csv(leads, directory / "leads.csv")
    export_markdown(leads, directory / "leads.md")
    export_json(leads, directory / "leads.json")
