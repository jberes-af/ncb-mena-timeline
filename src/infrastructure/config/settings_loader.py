# /src/infrastructure/config/settings_loader.py

# /src/infrastructure/config/settings_loader.py

from pathlib import Path

from src.infrastructure.config.google_settings_loader import (
    load_google_sheets_api_key,
    load_spreadsheet_ids,
)

from src.infrastructure.config.path_settings_loader import (
    resolve_config_path,
)

from src.infrastructure.config.secret_provider import SecretProvider

from src.infrastructure.config.settings_model import Settings


def load_settings(
        *,
        project_root: Path,
        secret_provider: SecretProvider,
) -> Settings:
    project_root = project_root.resolve()

    config_path = resolve_config_path(project_root)

    return Settings(
        project_root=project_root,
        config_path=config_path,
        google_sheets_api_key=load_google_sheets_api_key(secret_provider),
        spreadsheet_ids_by_file=load_spreadsheet_ids(secret_provider),
    )
