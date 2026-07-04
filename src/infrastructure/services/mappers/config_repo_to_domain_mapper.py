# /src/infrastructure/services/mappers/config_repo_to_domain_mapper.py

from src.domain.entities.entities import (
    ActorRecordDTO,
    CountryRecordDTO,
    CitationRecordDTO,
    EventActorDTO,
    EventDescriptionDTO,
    TimelineInputsDTO,
)

from src.infrastructure.persistence.google.sheets.repo_config_inputs.raw_sheets_models import (
    ActorRecordRaw,
    CountryRecordRaw,
    CitationRecordRaw,
    EventActorRaw,
    EventDescriptionRaw,
)


class RawSheetToDomainMapper:
    """
    Converts raw Google Sheet models into domain DTOs.

    Raw models should reflect Google Sheet column headers.
    Domain DTOs should contain application-ready types.
    """

    def to_timeline_inputs(
            self,
            *,
            actor_record_raw_items: list[ActorRecordRaw],
            country_record_raw_items: list[CountryRecordRaw],
            event_actor_raw_items: list[EventActorRaw],
            events_raw_items: list[EventDescriptionRaw],
            citation_raw_items: list[CitationRecordRaw],
    ) -> TimelineInputsDTO:
        return TimelineInputsDTO(
            actor_records=tuple(
                self._to_actor_record(raw_item)
                for raw_item in actor_record_raw_items
            ),
            country_records=tuple(
                self._to_country_record(raw_item)
                for raw_item in country_record_raw_items
            ),
            event_actors=tuple(
                self._to_event_actor(raw_item)
                for raw_item in event_actor_raw_items
            ),
            events=tuple(
                self._to_event_description(raw_item)
                for raw_item in events_raw_items
            ),
            citations=tuple(
                self._to_citation_record(raw_item)
                for raw_item in citation_raw_items
            ),
        )

    @staticmethod
    def _to_actor_record(raw_item: ActorRecordRaw) -> ActorRecordDTO:
        return ActorRecordDTO(
            actor_id=raw_item.actor_id,
            actor_reference=raw_item.actor_reference,
            is_country=_to_bool(raw_item.is_country),
            actor_name=raw_item.actor_name,
        )

    @staticmethod
    def _to_country_record(raw_item: CountryRecordRaw) -> CountryRecordDTO:
        return CountryRecordDTO(
            country_id=raw_item.country_id,
            abbreviation_2=raw_item.abbreviation_2,
            abbreviation_3=raw_item.abbreviation_3,
            country_name=raw_item.country_name,
            country_flag_unicode=raw_item.country_flag_unicode,
        )

    @staticmethod
    def _to_event_actor(raw_item: EventActorRaw) -> EventActorDTO:
        return EventActorDTO(
            table_id=raw_item.table_id,
            event_id=raw_item.event_id,
            actor_id=raw_item.actor_id,
        )

    @staticmethod
    def _to_event_description(
            raw_item: EventDescriptionRaw,
    ) -> EventDescriptionDTO:
        return EventDescriptionDTO(
            event_id=raw_item.event_id,
            event_description=raw_item.event_description,
            year=int(raw_item.year),
            month=_to_optional_int(raw_item.month),
        )

    @staticmethod
    def _to_citation_record(raw_item: CitationRecordRaw) -> CitationRecordDTO:
        return CitationRecordDTO(
            citation_id=raw_item.citation_id,
            footnote_number=int(raw_item.footnote_number),
            event_id=raw_item.event_id,
            citation=raw_item.citation,
        )


def _to_optional_int(value: str | None) -> int | None:
    if value is None:
        return None

    clean_value = str(value).strip()

    if clean_value == "" or clean_value == "---":
        return None

    return int(clean_value)


def _to_bool(value: bool | str) -> bool:
    if isinstance(value, bool):
        return value

    clean_value = str(value).strip().lower()

    if clean_value in {"true", "t", "yes", "y", "1"}:
        return True

    if clean_value in {"false", "f", "no", "n", "0"}:
        return False

    raise ValueError(f"Cannot convert value to bool: {value}")
