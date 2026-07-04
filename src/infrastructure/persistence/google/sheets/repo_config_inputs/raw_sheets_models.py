# /src/infrastructure/google/sheets/repo_config_inputs/raw_sheets_models.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ActorRecordRaw:
    actor_id: str
    actor_reference: str
    is_country: bool
    actor_name: str


@dataclass(frozen=True)
class CountryRecordRaw:
    country_id: str
    abbreviation_2: str
    abbreviation_3: str
    country_name: str
    country_flag_unicode: str
    color_1: str | None = None
    color_2: str | None = None


@dataclass(frozen=True)
class EventActorRaw:
    table_id: str
    event_id: str
    actor_id: str


@dataclass(frozen=True)
class EventDescriptionRaw:
    event_id: str
    event_description: str
    year: str
    month: str


@dataclass(frozen=True)
class CitationRecordRaw:
    citation_id: str
    footnote_number: str
    event_id: str
    citation: str
