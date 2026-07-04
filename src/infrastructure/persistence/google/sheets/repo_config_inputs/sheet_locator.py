# /src/infrastructure/persistence/google/sheets/repo_config_inputs/sheet_locator.py

from dataclasses import dataclass


@dataclass(frozen=True)
class GoogleSheetLocator:
    spreadsheet_id: str
    worksheet_name: str
    worksheet_range: str


@dataclass(frozen=True)
class TimelineInputSheetLocators:
    actors: GoogleSheetLocator
    actors_in_events: GoogleSheetLocator
    citations: GoogleSheetLocator
    countries: GoogleSheetLocator
    events: GoogleSheetLocator
