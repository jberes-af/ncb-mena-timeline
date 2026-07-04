# /src/application/dto/analytics_dtos.py

from dataclasses import dataclass


@dataclass(frozen=True)
class EntityReferenceCountDTO:
    entity_reference: str
    count: int


@dataclass(frozen=True)
class TimelineAnalyticsResultDTO:
    count_selected_countries: int
    count_actors_selected: int
    count_actors_involved: int
    entity_reference_counts: tuple[EntityReferenceCountDTO, ...]
    count_events: int
    count_years_in_timeline: int
    first_year: int | None
    last_year: int | None
    year_range: int
    count_citations: int
