# infrastructure/config/settings_loader.py

from pathlib import Path
from dotenv import load_dotenv
from typing import cast
import os

from src.infrastructure.config.settings_model import Settings, GoogleAccessMode, DriveAccessMode
from src.infrastructure.persistence.google.auth.oauth_scopes import combined_scopes


class SettingsError(RuntimeError):
    pass


def getenv_required(name: str) -> str:
    v = os.getenv(name)
    if not v or not v.strip():
        raise SettingsError(f"Missing required environment variable: {name}")
    return v.strip()


def load_settings_from_env(
        *,
        project_root: Path,
        google_sheet_file_name: str,
) -> Settings:
    project_root: Path = project_root.resolve()
    load_dotenv(project_root / ".env")

    # --- CONFIG JSON PATH

    config_dir: Path = (project_root / "config").resolve()
    app_config_json_path: Path = (config_dir / "config.json").resolve()

    print("FFFFFFFFFFFFF")
    print(app_config_json_path)
    print("FFFFFFFFFFFFF")

    if not app_config_json_path.exists():
        raise SettingsError(f"App config JSON not found: {app_config_json_path}")

    if not app_config_json_path.is_file():
        raise SettingsError(f"App config JSON not found: {app_config_json_path}")

    # --- SHEETS ACCESS MODE

    sheets_mode_raw = os.getenv("GOOGLE_ACCESS_MODE", "read").strip().lower()
    if sheets_mode_raw not in ("read", "write"):
        raise SettingsError("GOOGLE_ACCESS_MODE must be 'read' or 'write'")
    sheets_mode = cast(GoogleAccessMode, sheets_mode_raw)

    # --- DRIVE ACCESS MODE

    drive_mode_raw = os.getenv("DRIVE_ACCESS_MODE", "none").strip().lower()
    if drive_mode_raw not in ("none", "read", "write", "all"):
        raise SettingsError("DRIVE_ACCESS_MODE must be one of: none, read, write, all")
    drive_mode = cast(DriveAccessMode, drive_mode_raw)

    scopes = combined_scopes(sheets_mode=sheets_mode, drive_mode=drive_mode)

    # --- OAUTH SECRETS FILE

    client_secret_filename = getenv_required("GOOGLE_CLIENT_SECRET_ACCOUNTING")
    client_secret_json = (project_root / "secrets" / client_secret_filename).resolve()
    if not client_secret_json.exists():
        raise SettingsError(f"Client secret not found: {client_secret_json}")

    # --- GOOGLE TOKEN

    state_dir = (project_root / "state").resolve()
    state_dir.mkdir(parents=True, exist_ok=True)

    raw_token = os.getenv("GOOGLE_TOKEN_JSON")
    if raw_token:
        token_path = Path(raw_token)
        token_json = (token_path if token_path.is_absolute() else (project_root / token_path)).resolve()
    else:
        needs_write = (sheets_mode == "write") or (drive_mode in ("write", "all"))
        token_default = "token_write.json" if needs_write else "token_read.json"
        token_json = (state_dir / token_default).resolve()

    spreadsheet_ids_by_file = {
        google_sheet_file_name: getenv_required("SHEET_ID_CONFIG"),
        # "model_config": getenv_required("SHEET_ID_CONFIG"),
    }

    # GOOGLE DRIVE FOLDER

    drive_root = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")
    if drive_mode != "none" and not (drive_root and drive_root.strip()):
        raise SettingsError("GOOGLE_DRIVE_ROOT_FOLDER_ID is required when DRIVE_ACCESS_MODE != 'none'")

    return Settings(
        project_root=project_root,
        config_path=app_config_json_path,
        google_client_secret=client_secret_json,
        google_oauth_token_json=token_json,
        google_scopes=scopes,
        spreadsheet_ids_by_file=spreadsheet_ids_by_file,
        google_access_mode=sheets_mode,
        drive_access_mode=drive_mode,
    )
