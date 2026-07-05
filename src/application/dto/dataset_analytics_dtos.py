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
class EventClassificationDTO:
    relationship_types: tuple[str, ...]
    domains: tuple[str, ...]
    mechanisms: tuple[str, ...]
    outcomes: tuple[str, ...]


@dataclass(frozen=True)
class DatasetAnalyticsResultDTO:
    pair_rows: tuple[ActorPairDTO, ...]
    pair_counts: tuple[ActorPairCountDTO, ...]
