# /infrastructure/google/sheets/sheet_locator_resolver.py


from dataclasses import dataclass
from typing import Mapping

from src.application.ports.google_sheets_repos.google_sheets_repositories import (
    SheetLocator, SheetLocatorPort)
from src.infrastructure.config.app_config_models import SheetSpec

@dataclass(frozen=True)
class SheetLocatorResolver(SheetLocatorPort):
    tables: Mapping[str, SheetSpec]
    spreadsheet_ids_by_file: Mapping[str, str]

    def resolve(self, *, table_key: str) -> SheetLocator:
        spec = self.tables.get(table_key)
        if spec is None:
            raise KeyError(f"Unknown table_key: {table_key}")

        if not spec.file_name:
            raise KeyError(f"Table '{table_key}' missing file_name")

        spreadsheet_id = self.spreadsheet_ids_by_file.get(spec.file_name)
        if not spreadsheet_id:
            raise KeyError(f"No spreadsheet id configured for file_name='{spec.file_name}'")

        return SheetLocator(spreadsheet_id=spreadsheet_id, sheet_name=spec.worksheet_name)
