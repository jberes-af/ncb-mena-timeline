# /src/infrastructure/config/google_settings_loader.py

from src.infrastructure.config.secret_provider import SecretProvider


class GoogleSettingsError(RuntimeError):
    pass


def load_google_sheets_api_key(
        secret_provider: SecretProvider,
) -> str:
    return secret_provider.get_required("GOOGLE_SHEETS_API_KEY")


def load_spreadsheet_ids(
        secret_provider: SecretProvider,
) -> dict[str, str]:
    return {
        "mena-timeline-project": secret_provider.get_required("SHEET_ID_CONFIG")
    }


"""

from pathlib import Path
from typing import cast


from src.infrastructure.config.settings_model import (
    DriveAccessMode,
    GoogleAccessMode,
)
from src.infrastructure.persistence.google.auth.oauth_scopes import (
    combined_scopes,
)


def load_google_access_mode(
    secret_provider: SecretProvider,
) -> GoogleAccessMode:
    raw = secret_provider.get("GOOGLE_ACCESS_MODE", "read")
    mode = (raw or "read").strip().lower()

    if mode not in ("read", "write"):
        raise GoogleSettingsError(
            "GOOGLE_ACCESS_MODE must be 'read' or 'write'"
        )

    return cast(GoogleAccessMode, mode)


def load_drive_access_mode(
    secret_provider: SecretProvider,
) -> DriveAccessMode:
    raw = secret_provider.get("DRIVE_ACCESS_MODE", "none")
    mode = (raw or "none").strip().lower()

    if mode not in ("none", "read", "write", "all"):
        raise GoogleSettingsError(
            "DRIVE_ACCESS_MODE must be one of: none, read, write, all"
        )

    return cast(DriveAccessMode, mode)


def resolve_google_client_secret_path(
    *,
    project_root: Path,
    secret_provider: SecretProvider,
) -> Path | None:
    filename = secret_provider.get("GOOGLE_CLIENT_SECRET_ACCOUNTING")

    if not filename:
        return None

    path = (project_root / "secrets" / filename).resolve()

    if not path.exists():
        raise GoogleSettingsError(f"Client secret not found: {path}")

    return path


def resolve_google_token_path(
    *,
    project_root: Path,
    state_dir: Path,
    secret_provider: SecretProvider,
    google_access_mode: GoogleAccessMode,
    drive_access_mode: DriveAccessMode,
) -> Path:
    raw_token = secret_provider.get("GOOGLE_TOKEN_JSON")

    if raw_token:
        token_path = Path(raw_token)
        return (
            token_path
            if token_path.is_absolute()
            else project_root / token_path
        ).resolve()

    needs_write = (
        google_access_mode == "write"
        or drive_access_mode in ("write", "all")
    )

    token_default = "token_write.json" if needs_write else "token_read.json"
    return (state_dir / token_default).resolve()


def load_google_scopes(
    *,
    google_access_mode: GoogleAccessMode,
    drive_access_mode: DriveAccessMode,
) -> list[str]:
    return combined_scopes(
        sheets_mode=google_access_mode,
        drive_mode=drive_access_mode,
    )


def validate_drive_settings(
    *,
    secret_provider: SecretProvider,
    drive_access_mode: DriveAccessMode,
) -> None:
    drive_root = secret_provider.get("GOOGLE_DRIVE_ROOT_FOLDER_ID")

    if drive_access_mode != "none" and not drive_root:
        raise GoogleSettingsError(
            "GOOGLE_DRIVE_ROOT_FOLDER_ID is required "
            "when DRIVE_ACCESS_MODE != 'none'"
        )
"""
