# /src/main/composition_root.py

# /src/main/composition_root.py

from dataclasses import dataclass
from pathlib import Path
import logging
import os

from src.application.ports.google_sheets_repos.google_sheets_repositories import (
    ConfigInputsRepositoryPort,
)

from src.infrastructure.config.app_config_loader import AppConfigLoader
from src.infrastructure.config.app_config_models import AppRuntimeConfig
from src.infrastructure.config.secret_provider import (
    EnvSecretProvider,
    SecretProvider,
)

from src.infrastructure.config.settings_loader import load_settings
from src.infrastructure.config.settings_model import Settings

from src.main.compo_root_google_sheets_repo import (
    get_sheets_repository_timeline_inputs,
)


@dataclass(frozen=True)
class AppContainer:
    settings: Settings
    cfg: AppRuntimeConfig
    timeline_inputs_repository: ConfigInputsRepositoryPort


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _running_on_streamlit_cloud() -> bool:
    return bool(os.getenv("STREAMLIT_RUNTIME")) or bool(os.getenv("STREAMLIT_SERVER_PORT"))


def _build_secret_provider(
    *,
    project_root: Path,
) -> SecretProvider:
    if _running_on_streamlit_cloud():
        from src.gui.streamlit.streamlit_settings_loader import (
            StreamlitSecretProvider,
        )

        return StreamlitSecretProvider()

    return EnvSecretProvider(
        env_path=project_root / ".env",
    )


def load_runtime_config() -> tuple[Settings, AppRuntimeConfig]:
    project_root = resolve_project_root()

    logging.info("Project root resolved: %s", project_root)

    secret_provider = _build_secret_provider(
        project_root=project_root,
    )

    settings = load_settings(
        project_root=project_root,
        secret_provider=secret_provider,
    )

    logging.info("Settings loaded")

    cfg = AppConfigLoader.load_from_json(
        settings.config_path,
        project_root=project_root,
    )

    logging.info("Config loaded")

    return settings, cfg


def build_app_container() -> AppContainer:
    settings, cfg = load_runtime_config()

    timeline_inputs_repository = get_sheets_repository_timeline_inputs(
        settings=settings,
        cfg=cfg,
    )

    return AppContainer(
        settings=settings,
        cfg=cfg,
        timeline_inputs_repository=timeline_inputs_repository,
    )


app_container = build_app_container()
