# /src/application/dto/show_timeline_dtos.py

from dataclasses import dataclass

from src.domain.entities.entities import (
    TimelineInputsDTO,
    # EventDescriptionDTO,
)


@dataclass(frozen=True)
class ShowTimelineRequestDTO:
    timeline_inputs: TimelineInputsDTO
    selected_country_ids: tuple[str, ...]
    selected_actor_ids: tuple[str, ...]
    selected_years: tuple[int, ...]


@dataclass(frozen=True)
class TimelineEventViewDTO:
    year: int
    month: int | None
    event_description: str
    country_alpha2_codes: tuple[str, ...]
    # country_flags: tuple[str, ...]
    country_abbreviations: tuple[str, ...]
    citation_ids: tuple[str, ...]


@dataclass(frozen=True)
class ShowTimelineResultDTO:
    events: tuple[TimelineEventViewDTO, ...]
