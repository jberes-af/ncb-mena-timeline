# /src/interface_adapters/controllers/analytics_controller.py

from src.application.use_cases.use_cases_interactor import (
    RunAnalyticsUseCasesInteractor,
    # AnalyzeMovementPatternsInteractor,
)

from src.application.dto.run_analytics_use_cases_dtos import (
    RunAnalyticsUseCasesRequestDTO,
    RunAnalyticsUseCasesResultDTO,
)

import logging

logger = logging.getLogger(__name__)


class RunAnalyticsUseCasesController:
    def __init__(
            self,
            run_analysis_use_cases: RunAnalyticsUseCasesInteractor,
            # analyze_movements_use_case: AnalyzeMovementPatternsInteractor,
    ) -> None:
        self._run_analysis_use_cases = run_analysis_use_cases
        # self._analyze_movements_uc = analyze_movements_use_case

    def run(
            self,
            request: RunAnalyticsUseCasesRequestDTO,
    ) -> RunAnalyticsUseCasesResultDTO:

        logging.info("Starting orchestration use case...")

        result: RunAnalyticsUseCasesResultDTO = (
            self._run_analysis_use_cases.execute(request)
        )

        logging.info("   ... all use case executions complete.")

        return result
