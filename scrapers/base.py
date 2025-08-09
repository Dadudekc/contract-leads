"""Base classes for lead scrapers."""

from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Lead:
    """Representation of a single lead posting."""

    title: str
    url: str
    description: str
    posted: dt.datetime


class Scraper(ABC):
    """Abstract base class for scrapers."""

    @abstractmethod
    def fetch(self) -> List[Lead]:
        """Return a list of leads from the source."""
        raise NotImplementedError
