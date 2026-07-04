# /src/infrastructure/config/settings_model.py

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping, Sequence


GoogleAccessMode = Literal["read", "write"]
DriveAccessMode = Literal["none", "read", "write", "all"]


@dataclass(frozen=True)
class Settings:
    project_root: Path
    config_path: Path

    google_client_secret: Path
    google_oauth_token_json: Path
    google_scopes: Sequence[str]

    spreadsheet_ids_by_file: Mapping[str, str]
    google_access_mode: GoogleAccessMode
    drive_access_mode: DriveAccessMode
    # google_drive_root_folder_id: str | None = None
    # google_places_api_key: str
