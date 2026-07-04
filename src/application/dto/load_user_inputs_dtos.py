# /src/application/dtos/load_user_inputs_dtos.py

from dataclasses import dataclass

from src.domain.entities.entities import (
    ActorRecordDTO,
    CountryRecordDTO,
    EventDescriptionDTO,
)


@dataclass(frozen=True)
class UserInputRequestDTO:
    scenario_name: str


@dataclass(frozen=True)
class UserInputResultDTO:
    selected_actors: list[ActorRecordDTO]
    selected_countries: list[CountryRecordDTO]
    selected_year: list[str]
