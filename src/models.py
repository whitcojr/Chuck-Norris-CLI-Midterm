"""Data models for the Chuck Norris CLI.

Small dataclasses that map to API responses. Keep them lightweight so
they are easy to construct from the API JSON and simple to test.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Joke:
    id: str
    value: str
    url: Optional[str] = None
    icon_url: Optional[str] = None
    categories: List[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Joke":
        return cls(
            id=data.get("id", ""),
            value=data.get("value", ""),
            url=data.get("url"),
            icon_url=data.get("icon_url"),
            categories=data.get("categories") or [],
        )


@dataclass
class SearchResults:
    total: int
    result: List[Joke]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SearchResults":
        items = []
        for it in data.get("result", []):
            items.append(Joke.from_dict(it))
        return cls(total=int(data.get("total", len(items))), result=items)
