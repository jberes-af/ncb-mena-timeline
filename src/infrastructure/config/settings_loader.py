# /src/infrastructure/config/settings_loader.py

from pathlib import Path
from typing import cast
import json
import os

from dotenv import load_dotenv

from src.infrastructure.config.settings_model import (
    Settings,
    GoogleAccessMode,
    DriveAccessMode,
)

from src.infrastructure.persistence.google.auth.oauth_scopes import (
    combined_scopes,
)


class SettingsError(RuntimeError):
    pass


def load_settings_from_env(
    *,
    project_root: Path,
    google_sheet_file_name: str,
) -> Settings:
    project_root = project_root.resolve()
    load_dotenv(project_root / ".env")

    app_config_json_path = project_root / "config" / "config.json"

    if not app_config_json_path.is_file():
        raise SettingsError(
            f"App config JSON not found: {app_config_json_path}"
        )

    sheets_mode_raw = _get_setting(
        "GOOGLE_ACCESS_MODE",
        default="read",
    ).strip().lower()

    if sheets_mode_raw not in ("read", "write"):
        raise SettingsError("GOOGLE_ACCESS_MODE must be 'read' or 'write'")

    sheets_mode = cast(GoogleAccessMode, sheets_mode_raw)

    drive_mode_raw = _get_setting(
        "DRIVE_ACCESS_MODE",
        default="none",
    ).strip().lower()

    if drive_mode_raw not in ("none", "read", "write", "all"):
        raise SettingsError(
            "DRIVE_ACCESS_MODE must be one of: none, read, write, all"
        )

    drive_mode = cast(DriveAccessMode, drive_mode_raw)

    scopes = combined_scopes(
        sheets_mode=sheets_mode,
        drive_mode=drive_mode,
    )

    google_client_secret = _load_google_client_secret(
        project_root=project_root,
    )

    google_oauth_token_json = _load_google_token_json(
        project_root=project_root,
        sheets_mode=sheets_mode,
        drive_mode=drive_mode,
    )

    spreadsheet_ids_by_file = {
        google_sheet_file_name: _get_required_setting("SHEET_ID_CONFIG"),
    }

    drive_root = _get_setting("GOOGLE_DRIVE_ROOT_FOLDER_ID")

    if drive_mode != "none" and not drive_root:
        raise SettingsError(
            "GOOGLE_DRIVE_ROOT_FOLDER_ID is required when "
            "DRIVE_ACCESS_MODE != 'none'"
        )

    return Settings(
        project_root=project_root,
        config_path=app_config_json_path,
        google_client_secret=google_client_secret,
        google_oauth_token_json=google_oauth_token_json,
        google_scopes=scopes,
        spreadsheet_ids_by_file=spreadsheet_ids_by_file,
        google_access_mode=sheets_mode,
        drive_access_mode=drive_mode,
    )


def _running_in_streamlit() -> bool:
    try:
        import streamlit as st

        return bool(st.secrets)
    except Exception:
        return False


def _get_setting(
    name: str,
    default: str | None = None,
) -> str | None:
    value = os.getenv(name)

    if value and value.strip():
        return value.strip()

    if _running_in_streamlit():
        import streamlit as st

        if name in st.secrets:
            return str(st.secrets[name]).strip()

    return default


def _get_required_setting(name: str) -> str:
    value = _get_setting(name)

    if not value:
        raise SettingsError(f"Missing required setting: {name}")

    return value


def _load_google_client_secret(
    *,
    project_root: Path,
) -> dict:
    if _running_in_streamlit():
        import streamlit as st

        google = st.secrets["google_oauth_client"]

        return {
            "installed": {
                "client_id": google["client_id"],
                "project_id": google["project_id"],
                "auth_uri": google["auth_uri"],
                "token_uri": google["token_uri"],
                "auth_provider_x509_cert_url": google[
                    "auth_provider_x509_cert_url"
                ],
                "client_secret": google["client_secret"],
                "redirect_uris": list(google["redirect_uris"]),
            }
        }

    client_secret_filename = _get_required_setting(
        "GOOGLE_CLIENT_SECRET_ACCOUNTING"
    )

    client_secret_path = (
        project_root / "secrets" / client_secret_filename
    ).resolve()

    if not client_secret_path.is_file():
        raise SettingsError(f"Client secret not found: {client_secret_path}")

    with client_secret_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_google_token_json(
    *,
    project_root: Path,
    sheets_mode: GoogleAccessMode,
    drive_mode: DriveAccessMode,
) -> Path | dict:
    if _running_in_streamlit():
        import streamlit as st

        return dict(st.secrets["google_oauth_token"])

    state_dir = project_root / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    raw_token = os.getenv("GOOGLE_TOKEN_JSON")

    if raw_token:
        token_path = Path(raw_token)
        return (
            token_path
            if token_path.is_absolute()
            else project_root / token_path
        ).resolve()

    needs_write = (
        sheets_mode == "write"
        or drive_mode in ("write", "all")
    )

    token_default = "token_write.json" if needs_write else "token_read.json"

    return (state_dir / token_default).resolve()
