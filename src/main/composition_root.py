# /src/main/composition_root.py

from dataclasses import dataclass
from pathlib import Path
import logging

from src.infrastructure.config.settings_loader import load_settings_from_env
from src.infrastructure.config.app_config_loader import AppConfigLoader
from src.infrastructure.config.settings_model import Settings
from src.infrastructure.config.app_config_models import AppRuntimeConfig

from src.infrastructure.firebase.firebase_client_auth_service import FirebaseClientAuthService
from src.application.auth.login_user import LoginUser
from src.interface_adapters.controllers.auth_controller import AuthController
from src.interface_adapters.presenters.auth_presenter import AuthPresenter


@dataclass(frozen=True)
class AppContainer:
    settings: Settings
    cfg: AppRuntimeConfig
    auth_controller: AuthController
    auth_presenter: AuthPresenter


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_runtime_config() -> tuple[Settings, AppRuntimeConfig]:
    project_root = resolve_project_root()

    logging.info("Project root resolved: %s", project_root)

    settings = load_settings_from_env(project_root=project_root)
    logging.info("Settings loaded")

    cfg = AppConfigLoader.load_from_json(
        settings.config_path,
        project_root=project_root,
    )
    logging.info("Config loaded")

    return settings, cfg


def build_app_container() -> AppContainer:
    settings, cfg = load_runtime_config()

    """
    firebase_auth_provider = FirebaseAuthProvider(
        pyrebase_config=cfg.firebase.pyrebase_config,
        service_account_info=cfg.firebase.service_account_info,
    )
    """

    firebase_client_auth_service = FirebaseClientAuthService(
        web_config=dict(settings.firebase_web.to_pyrebase_config()),
    )

    login_user = LoginUser(
        auth_provider=firebase_client_auth_service,
    )

    auth_controller = AuthController(
        login_user=login_user,
    )

    auth_presenter = AuthPresenter()

    return AppContainer(
        settings=settings,
        cfg=cfg,
        auth_controller=auth_controller,
        auth_presenter=auth_presenter,
    )


app_container = build_app_container()
