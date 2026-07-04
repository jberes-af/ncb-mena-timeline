# /src/interface_adapters/controllers/startup_controller.py

from src.application.use_cases.use_cases_interactor import (
    RunStartupUseCasesInteractor,
)

from src.application.dto.run_startup_use_cases_dtos import (
    RunStartupUseCasesRequestDTO,
    RunStartupUseCasesResultDTO,
)

import logging

logger = logging.getLogger(__name__)


class RunStartupUseCasesController:
    def __init__(
            self,
            run_startup_use_cases: RunStartupUseCasesInteractor,
    ) -> None:
        self._run_startup_use_cases = run_startup_use_cases

    def run(
            self,
            request: RunStartupUseCasesRequestDTO,
    ) -> RunStartupUseCasesResultDTO:

        logging.info("Starting orchestration use case...")

        result: RunStartupUseCasesResultDTO = (
            self._run_startup_use_cases.execute(request)
        )

        logging.info("   ... startup use case executions complete.")

        return result
