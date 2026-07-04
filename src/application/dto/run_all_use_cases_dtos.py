# /src/application/dto/run_all_use_cases_dtos.py

from dataclasses import dataclass

from src.domain.entities.entities import TimelineInputsDTO

from src.application.dto.show_timeline_dtos import (
    ShowTimelineResultDTO,
)


@dataclass(frozen=True)
class RunAllUseCasesRequestDTO:
    timeline_inputs: TimelineInputsDTO
    selected_country_ids: tuple[str, ...]
    selected_years: tuple[int, ...]


@dataclass(frozen=True)
class RunAllUseCasesResultDTO:
    run_all_request: RunAllUseCasesRequestDTO
    show_timeline_result: ShowTimelineResultDTO