# /src/application/use_cases/dataset_analytics_use_case.py

from collections import Counter, defaultdict
from itertools import combinations

from src.domain.entities.entities import TimelineInputsDTO, EventActorDTO

from src.application.dto.dataset_analytics_dtos import (
    ActorPairDTO,
    ActorPairCountDTO,
    DatasetAnalyticsResultDTO,
)

from dataclasses import asdict
from pathlib import Path
import csv


class DatasetAnalyticsUseCase:
    def execute(
            self,
            *,
            timeline_inputs: TimelineInputsDTO,
            project_root: Path | None = None,
    ) -> DatasetAnalyticsResultDTO:
        event_actor_map = _build_event_actor_mapping(
            event_actors=timeline_inputs.event_actors,
        )

        pair_rows: list[ActorPairDTO] = _generate_actor_pairings(
            event_actor_map=event_actor_map,
        )

        pair_counter = Counter(
            (row.actor_1, row.actor_2)
            for row in pair_rows
        )

        actor_by_id = {
            actor.actor_id: actor
            for actor in timeline_inputs.actor_records
        }

        country_by_id = {
            country.country_id: country
            for country in timeline_inputs.country_records
        }

        pair_counts: list[ActorPairCountDTO] = _build_pair_counts(
            pair_counter=pair_counter,
            actor_by_id=actor_by_id,
            country_by_id=country_by_id,
        )

        """
        FOR DEV ONLY - do not write to local file when Streamlit hosted 
        _export_actor_pair_rows(
            rows=pair_rows,
            output_path=project_root / "data/results" / "event_actor_pairs.csv",
        )
        """

        return DatasetAnalyticsResultDTO(
            pair_rows=tuple(pair_rows),
            pair_counts=tuple(pair_counts),
        )


def _build_event_actor_mapping(
        *,
        event_actors: tuple[EventActorDTO, ...],
) -> dict[str, list[str]]:
    event_actor_map: dict[str, list[str]] = defaultdict(list)

    for event_actor in event_actors:
        event_actor_map[event_actor.event_id].append(event_actor.actor_id)

    return dict(event_actor_map)


def _generate_actor_pairings(
        *,
        event_actor_map: dict[str, list[str]],
) -> list[ActorPairDTO]:
    pair_rows: list[ActorPairDTO] = []

    for event_id, actor_ids in event_actor_map.items():
        unique_actor_ids = sorted(set(actor_ids))

        for actor_1, actor_2 in combinations(unique_actor_ids, 2):
            pair_rows.append(
                ActorPairDTO(
                    event_id=event_id,
                    actor_1=actor_1,
                    actor_2=actor_2,
                )
            )

    return pair_rows


def _build_pair_counts(
        *,
        pair_counter: Counter[tuple[str, str]],
        actor_by_id,
        country_by_id,
) -> list[ActorPairCountDTO]:
    return [
        ActorPairCountDTO(
            actor_1_id=pair[0],
            actor_1_label=_actor_label(pair[0], actor_by_id, country_by_id),
            actor_2_id=pair[1],
            actor_2_label=_actor_label(pair[1], actor_by_id, country_by_id),
            count=count,
        )
        for pair, count in sorted(
            pair_counter.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]


def _actor_label(actor_id: str, actor_by_id, country_by_id) -> str:
    actor = actor_by_id.get(actor_id)

    if actor is None:
        return actor_id

    if actor.is_country:
        country = country_by_id.get(actor.actor_reference)
        return country.abbreviation_3 if country else actor.actor_reference

    return actor.actor_reference or actor.actor_name


def _export_actor_pair_rows(
        *,
        rows: list[ActorPairDTO],
        output_path: Path,
) -> None:
    with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
    ) as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=[
                "event_id",
                "actor_1",
                "actor_2",
            ],
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(asdict(row))


"""
def _export_actor_pair_counts(
        *,
        rows: list[ActorPairDTO],
        output_path: Path,
) -> None:
    with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
    ) as fp:

        writer = csv.DictWriter(
            fp,
            fieldnames=[
                "actor_1",
                "actor_2",
                "count",
            ],
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(asdict(row))
"""
