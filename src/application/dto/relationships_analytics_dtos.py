# /src/application/dto/relationships_analytics_dtos.py

from dataclasses import dataclass


@dataclass(frozen=True)
class EventClassificationDTO:
    relationship_types: tuple[str, ...]
    domains: tuple[str, ...]
    interactions: tuple[str, ...]
    outcomes: tuple[str, ...]


@dataclass(frozen=True)
class RelationshipsAnalyticsResultDTO:
    pass
