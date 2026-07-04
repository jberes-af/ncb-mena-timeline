# /src/application/use_cases/use_cases_interactor.py
# /src/application/use_cases/use_cases_interactor.py

from typing import Protocol
import logging

from src.application.dto.run_all_use_cases_dtos import (
    RunAllUseCasesRequestDTO,
    RunAllUseCasesResultDTO,
)

from src.application.dto.show_timeline_dtos import (
    ShowTimelineRequestDTO,
    ShowTimelineResultDTO,
)

logger = logging.getLogger(__name__)


class ShowTimelineInteractor(Protocol):
    def execute(
        self,
        request: ShowTimelineRequestDTO,
    ) -> ShowTimelineResultDTO:
        ...


class RunAllUseCasesInteractor:
    def __init__(
        self,
        show_timeline_use_case: ShowTimelineInteractor,
    ) -> None:
        self._show_timeline_uc = show_timeline_use_case

    def execute(
        self,
        request: RunAllUseCasesRequestDTO,
    ) -> RunAllUseCasesResultDTO:
        logger.info("Running timeline use case...")

        show_timeline_result: ShowTimelineResultDTO = (
            self._show_timeline_uc.execute(
                ShowTimelineRequestDTO(
                    timeline_inputs=request.timeline_inputs,
                    selected_country_ids=request.selected_country_ids,
                    selected_years=request.selected_years,
                )
            )
        )

        logger.info("Timeline use case complete.")

        return RunAllUseCasesResultDTO(
            run_all_request=request,
            show_timeline_result=show_timeline_result,
        )
