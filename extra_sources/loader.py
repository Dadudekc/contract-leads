"""Utilities for discovering extra scrapers."""

from __future__ import annotations

from importlib import import_module
from inspect import isclass
from pathlib import Path
from typing import List

from scrapers.base import Scraper


def load_extra_scrapers() -> List[Scraper]:
    """Dynamically load ``Scraper`` subclasses from the ``extra_sources`` package."""
    scrapers: List[Scraper] = []
    pkg_path = Path(__file__).parent
    for py_file in pkg_path.glob("*.py"):
        if py_file.name in {"__init__.py", "loader.py"}:
            continue
        module_name = f"{pkg_path.name}.{py_file.stem}"
        module = import_module(module_name)
        for obj in module.__dict__.values():
            if isclass(obj) and issubclass(obj, Scraper) and obj is not Scraper:
                scrapers.append(obj())
    return scrapers
