# /src/application/dto/dataset_analytics_dtos.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ActorPairDTO:
    event_id: str
    actor_1: str
    actor_2: str


@dataclass(frozen=True)
class ActorPairCountDTO:
    actor_1_id: str
    actor_1_label: str
    actor_2_id: str
    actor_2_label: str
    count: int



@dataclass(frozen=True)
class DatasetStatisticsDTO:
    count_countries: int
    count_actors: int
    count_events: int
    count_citations: int
    first_year: int | None = None
    last_year: int | None = None
    year_range: int | None = None


"""
@dataclass(frozen=True)
class EventClassificationDTO:
    relationship_types: tuple[str, ...]
    domains: tuple[str, ...]
    mechanisms: tuple[str, ...]
    outcomes: tuple[str, ...]
"""

@dataclass(frozen=True)
class DatasetAnalyticsResultDTO:
    dataset_statistics: DatasetStatisticsDTO
    pair_rows: tuple[ActorPairDTO, ...]
    pair_counts: tuple[ActorPairCountDTO, ...]
