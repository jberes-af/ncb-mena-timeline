# /src/infrastructure/persistence/google/sheets/repo_config_inputs/config_repo_adapter.py

from dataclasses import dataclass

from src.domain.entities.entities import TimelineInputsDTO

from src.application.ports.google_sheets_repos.google_sheets_repositories import (
    ConfigInputsRepositoryPort,
)

from src.infrastructure.persistence.google.sheets.sheets_query_service import (
    GoogleSheetsQueryService,
)

from src.infrastructure.persistence.google.sheets.repo_config_inputs.sheet_locator import (
    GoogleSheetLocator,
    TimelineInputSheetLocators,
)

from src.infrastructure.persistence.google.sheets.repo_config_inputs.raw_sheets_models import (
    ActorRecordRaw,
    CountryRecordRaw,
    CitationRecordRaw,
    EventDescriptionRaw,
    EventActorRaw,
)

from src.infrastructure.services.mappers.config_repo_to_domain_mapper import (
    RawSheetToDomainMapper,
)

from src.infrastructure.services.mappers.raw_sheet_parser import (
    parse_rows_to_raw_models,
)


@dataclass
class ConfigInputsGoogleSheetsRepository(ConfigInputsRepositoryPort):
    query_service: GoogleSheetsQueryService
    locators: TimelineInputSheetLocators
    mapper: RawSheetToDomainMapper

    def load_timeline_inputs(self) -> TimelineInputsDTO:
        """
        Load timeline input tables from Google Sheets.

        Pipeline:
        Google Sheets -> list[dict[str, str]] -> Raw dataclasses -> Domain DTO
        """

        rows_actors: list[dict[str, str]] = self._get_table(
            name="actors",
            locator=self.locators.actors,
        )

        rows_countries: list[dict[str, str]] = self._get_table(
            name="countries",
            locator=self.locators.countries,
        )

        rows_citations: list[dict[str, str]] = self._get_table(
            name="citations",
            locator=self.locators.citations,
        )

        rows_actors_in_events: list[dict[str, str]] = self._get_table(
            name="actors_in_events",
            locator=self.locators.actors_in_events,
        )

        rows_events: list[dict[str, str]] = self._get_table(
            name="events",
            locator=self.locators.events,
        )

        raw_actors: list[ActorRecordRaw] = parse_rows_to_raw_models(
            rows=rows_actors,
            model_cls=ActorRecordRaw,
        )

        raw_countries: list[CountryRecordRaw] = parse_rows_to_raw_models(
            rows=rows_countries,
            model_cls=CountryRecordRaw,
        )

        raw_citations: list[CitationRecordRaw] = parse_rows_to_raw_models(
            rows=rows_citations,
            model_cls=CitationRecordRaw,
        )

        raw_event_actors: list[EventActorRaw] = parse_rows_to_raw_models(
            rows=rows_actors_in_events,
            model_cls=EventActorRaw,
        )

        raw_events: list[EventDescriptionRaw] = parse_rows_to_raw_models(
            rows=rows_events,
            model_cls=EventDescriptionRaw,
        )

        return self.mapper.to_timeline_inputs(
            actor_record_raw_items=raw_actors,
            country_record_raw_items=raw_countries,
            event_actor_raw_items=raw_event_actors,
            events_raw_items=raw_events,
            citation_raw_items=raw_citations,
        )

    def _get_table(
            self,
            *,
            name: str,
            locator: GoogleSheetLocator,
    ) -> list[dict[str, str]]:
        spreadsheet_id: str = locator.spreadsheet_id

        if not spreadsheet_id:
            raise KeyError(
                f"No spreadsheet_id configured for worksheet '{name}'."
            )

        tab_name: str = locator.worksheet_name
        worksheet_range: str = locator.worksheet_range
        range_a1: str = f"{tab_name}!{worksheet_range}"

        return self.query_service.read_values(
            spreadsheet_id=spreadsheet_id,
            range_a1=range_a1,
        )
