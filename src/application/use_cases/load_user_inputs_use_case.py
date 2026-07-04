# /src/application/use_cases/load_user_inputs_use_case.py


from src.domain.entities.entities import (
    CountryRecordDTO,
    EventActorDTO,
    EventDescriptionDTO,
    CitationRecordDTO,
)

from src.application.dto.load_user_inputs_dtos import (
    UserInputRequestDTO,
    UserInputResultDTO,
)


class BuildSelectedUserInputsUseCase:
    def __init__(
            self,
    ) -> None:
        pass

    def execute(
            self,
            request: UserInputRequestDTO,
    ) -> UserInputResultDTO:
        return UserInputResultDTO(
            scenario_name="",
        )
