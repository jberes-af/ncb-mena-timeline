# /src/interface_adapters/controllers/program_controller.py

# /src/interface_adapters/controllers/program_controller.py

import logging

from src.application.use_cases.use_cases_interactor import (
    RunAllUseCasesInteractor,
)

from src.application.dto.run_all_use_cases_dtos import (
    RunAllUseCasesRequestDTO,
    RunAllUseCasesResultDTO,
)

logger = logging.getLogger(__name__)


class RunAllUseCasesController:
    def __init__(
        self,
        run_all_use_cases: RunAllUseCasesInteractor,
    ) -> None:
        self._run_all_use_cases = run_all_use_cases

    def run(
        self,
        request: RunAllUseCasesRequestDTO,
    ) -> RunAllUseCasesResultDTO:
        logger.info("Starting orchestration use case...")

        result: RunAllUseCasesResultDTO = (
            self._run_all_use_cases.execute(request)
        )

        logger.info("All use case executions complete.")

        return result
