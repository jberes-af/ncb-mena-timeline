# application/ports/google_sheets_repository.py

from dataclasses import dataclass
from typing import Protocol

from src.domain.entities.entities import TimelineInputsDTO


@dataclass(frozen=True)
class SheetLocator:
    spreadsheet_id: str
    sheet_name: str


class SheetLocatorPort(Protocol):
    def resolve(self, *, table_key: str) -> SheetLocator:
        ...


class ConfigInputsRepositoryPort(Protocol):
    def load_timeline_inputs(self) -> TimelineInputsDTO:
        ...
        # Load timeline inputs from an external source.
