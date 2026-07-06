# /src/application/use_cases/show_timeline_use_case.py

from src.domain.entities.entities import (
    ActorRecordDTO,
    EventActorDTO,
)

from src.application.dto.show_timeline_dtos import (
    CitationViewDTO,
    ShowTimelineRequestDTO,
    ShowTimelineResultDTO,
    TimelineEventViewDTO,
)


class ShowTimelineUseCase:
    def execute(
        self,
        request: ShowTimelineRequestDTO,
    ) -> ShowTimelineResultDTO:
        inputs = request.timeline_inputs

        selected_actor_ids = set(request.selected_actor_ids)
        selected_country_ids = set(request.selected_country_ids)
        selected_years = set(request.selected_years)

        event_by_id = {
            event.event_id: event
            for event in inputs.events
        }

        actor_by_id = {
            actor.actor_id: actor
            for actor in inputs.actor_records
        }

        country_by_id = {
            country.country_id: country
            for country in inputs.country_records
        }

        actor_ids_by_event_id = self._build_actor_ids_by_event_id(
            event_actors=inputs.event_actors,
        )

        citations_by_event_id = self._build_citations_by_event_id(
            citation_records=inputs.citations,
        )

        matching_event_ids = self._find_matching_event_ids(
            actor_ids_by_event_id=actor_ids_by_event_id,
            actor_by_id=actor_by_id,
            selected_actor_ids=selected_actor_ids,
            selected_country_ids=selected_country_ids,
        )

        timeline_events: list[TimelineEventViewDTO] = []

        for event_id in matching_event_ids:
            event = event_by_id.get(event_id)

            if event is None:
                continue

            if event.year not in selected_years:
                continue

            all_actor_ids_for_event = actor_ids_by_event_id.get(event_id, [])

            country_alpha2_codes: list[str] = []
            entity_references: list[str] = []

            for actor_id in all_actor_ids_for_event:
                actor = actor_by_id.get(actor_id)

                if actor is None:
                    continue

                if actor.is_country:
                    country = country_by_id.get(actor.actor_reference)

                    if country is None:
                        continue

                    country_alpha2_codes.append(country.abbreviation_2)
                    entity_references.append(country.abbreviation_3)

                else:
                    entity_references.append(actor.actor_reference)

            timeline_events.append(
                TimelineEventViewDTO(
                    year=event.year,
                    month=event.month,
                    event_description=event.event_description,
                    country_alpha2_codes=tuple(country_alpha2_codes),
                    country_abbreviations=tuple(entity_references),
                    citations=tuple(
                        citations_by_event_id.get(event.event_id, [])
                    ),
                    event_id_label=event.event_id,
                )
            )

        timeline_events.sort(
            key=lambda item: (
                item.year,
                item.month or 0,
                item.event_description,
            )
        )

        return ShowTimelineResultDTO(

            events=tuple(timeline_events),
        )

    @staticmethod
    def _build_actor_ids_by_event_id(
        *,
        event_actors: tuple[EventActorDTO, ...],
    ) -> dict[str, list[str]]:
        actor_ids_by_event_id: dict[str, list[str]] = {}

        for event_actor in event_actors:
            actor_ids_by_event_id.setdefault(
                event_actor.event_id,
                [],
            ).append(event_actor.actor_id)

        return actor_ids_by_event_id

    @staticmethod
    def _build_citation_ids_by_event_id(
        *,
        citation_records,
    ) -> dict[str, list[str]]:
        citation_ids_by_event_id: dict[str, list[str]] = {}

        for citation in citation_records:
            citation_ids_by_event_id.setdefault(
                citation.event_id,
                [],
            ).append(citation.citation_id)

        return citation_ids_by_event_id

    @staticmethod
    def _find_matching_event_ids(
        *,
        actor_ids_by_event_id: dict[str, list[str]],
        actor_by_id: dict[str, ActorRecordDTO],
        selected_actor_ids: set[str],
        selected_country_ids: set[str],
    ) -> set[str]:
        matching_event_ids: set[str] = set()

        for event_id, actor_ids in actor_ids_by_event_id.items():
            for actor_id in actor_ids:
                actor = actor_by_id.get(actor_id)

                if actor is None:
                    continue

                if actor_id in selected_actor_ids:
                    matching_event_ids.add(event_id)
                    break

                if actor.is_country and actor.actor_reference in selected_country_ids:
                    matching_event_ids.add(event_id)
                    break

        return matching_event_ids

    @staticmethod
    def _build_citations_by_event_id(
            *,
            citation_records,
    ) -> dict[str, list[CitationViewDTO]]:
        citations_by_event_id: dict[str, list[CitationViewDTO]] = {}

        for citation in citation_records:
            citations_by_event_id.setdefault(
                citation.event_id,
                [],
            ).append(
                CitationViewDTO(
                    citation_id=citation.citation_id,
                    citation_text=citation.citation,
                )
            )

        return citations_by_event_id