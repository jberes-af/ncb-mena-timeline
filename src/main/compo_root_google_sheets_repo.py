# /src/main/compo_root_google_sheets_repo.py

# /src/main/compo_root_google_sheets_repo.py

from src.application.ports.google_sheets_repos.google_sheets_repositories import (
    ConfigInputsRepositoryPort,
)

from src.infrastructure.config.settings_model import Settings
from src.infrastructure.config.app_config_models import AppRuntimeConfig

from src.infrastructure.persistence.google.sheets.public_sheets_query_service import (
    PublicGoogleSheetsQueryService,
)

from src.infrastructure.persistence.google.sheets.repo_config_inputs.sheet_locator import (
    GoogleSheetLocator,
    TimelineInputSheetLocators,
)

from src.infrastructure.persistence.google.sheets.repo_config_inputs.config_repo_adapter import (
    ConfigInputsGoogleSheetsRepository,
)

from src.infrastructure.services.mappers.config_repo_to_domain_mapper import (
    RawSheetToDomainMapper,
)


def get_sheets_repository_timeline_inputs(
    *,
    settings: Settings,
    cfg: AppRuntimeConfig,
) -> ConfigInputsRepositoryPort:
    query_service = _build_google_sheets_query_service(settings=settings)
    mapper = _build_google_sheets_repo_to_domain_mapper()

    return _build_config_inputs_repository(
        settings=settings,
        app_config=cfg,
        query_service=query_service,
        mapper=mapper,
    )


def _build_google_sheets_query_service(
    *,
    settings: Settings,
) -> PublicGoogleSheetsQueryService:
    return PublicGoogleSheetsQueryService(
        api_key=settings.google_sheets_api_key,
    )


def _build_google_sheets_repo_to_domain_mapper() -> RawSheetToDomainMapper:
    return RawSheetToDomainMapper()


def _build_config_inputs_repository(
    *,
    settings: Settings,
    app_config: AppRuntimeConfig,
    query_service: PublicGoogleSheetsQueryService,
    mapper: RawSheetToDomainMapper,
) -> ConfigInputsRepositoryPort:
    locators = TimelineInputSheetLocators(
        actors=_build_locator(
            settings=settings,
            app_config=app_config,
            table_name="actors",
        ),
        actors_in_events=_build_locator(
            settings=settings,
            app_config=app_config,
            table_name="actors_in_events",
        ),
        citations=_build_locator(
            settings=settings,
            app_config=app_config,
            table_name="citations",
        ),
        countries=_build_locator(
            settings=settings,
            app_config=app_config,
            table_name="countries",
        ),
        events=_build_locator(
            settings=settings,
            app_config=app_config,
            table_name="events",
        ),
    )

    return ConfigInputsGoogleSheetsRepository(
        query_service=query_service,
        locators=locators,
        mapper=mapper,
    )


def _build_locator(
    *,
    settings: Settings,
    app_config: AppRuntimeConfig,
    table_name: str,
) -> GoogleSheetLocator:
    table_config = app_config.google_sheets.tables.get(table_name)

    if table_config is None:
        raise KeyError(f"Missing Google Sheets table config: {table_name}")

    spreadsheet_id = settings.spreadsheet_ids_by_file.get(
        table_config.file_name,
    )

    if not spreadsheet_id:
        raise KeyError(
            f"No spreadsheet_id found for file_name: {table_config.file_name}"
        )

    return GoogleSheetLocator(
        spreadsheet_id=spreadsheet_id,
        worksheet_name=table_config.worksheet_name,
        worksheet_range=table_config.worksheet_range,
    )
