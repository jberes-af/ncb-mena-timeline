# /src/application/use_cases/show_timeline_use_case.py

from src.application.dto.show_timeline_dtos import (
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

        country_by_id = {
            country.country_id: country
            for country in inputs.country_records
        }

        actor_by_id = {
            actor.actor_id: actor
            for actor in inputs.actor_records
        }

        event_actors_by_event_id: dict[str, list[str]] = {}

        for event_actor in inputs.event_actors:
            event_actors_by_event_id.setdefault(
                event_actor.event_id,
                [],
            ).append(event_actor.actor_id)

        citation_ids_by_event_id: dict[str, list[str]] = {}

        for citation in inputs.citations:
            citation_ids_by_event_id.setdefault(
                citation.event_id,
                [],
            ).append(citation.citation_id)

        selected_country_ids = set(request.selected_country_ids)
        selected_years = set(request.selected_years)

        timeline_events: list[TimelineEventViewDTO] = []

        for event in inputs.events:
            if event.year not in selected_years:
                continue

            actor_ids = event_actors_by_event_id.get(event.event_id, [])

            event_country_ids: list[str] = []

            for actor_id in actor_ids:
                actor = actor_by_id.get(actor_id)

                if actor is None:
                    continue

                if not actor.is_country:
                    continue

                event_country_ids.append(actor.actor_reference)

            matching_country_ids = [
                country_id
                for country_id in event_country_ids
                if country_id in selected_country_ids
            ]

            if not matching_country_ids:
                continue

            countries = [
                country_by_id[country_id]
                for country_id in matching_country_ids
                if country_id in country_by_id
            ]

            country_alpha2_codes = tuple(
                country.abbreviation_2
                for country in countries
            )

            timeline_events.append(
                TimelineEventViewDTO(
                    year=event.year,
                    month=event.month,
                    event_description=event.event_description,
                    country_alpha2_codes=tuple(
                        country.abbreviation_2
                        for country in countries
                    ),
                    country_flags=tuple(
                        country.country_flag_unicode
                        for country in countries
                    ),
                    country_abbreviations=tuple(
                        country.abbreviation_3
                        for country in countries
                    ),
                    citation_ids=tuple(
                        citation_ids_by_event_id.get(event.event_id, [])
                    ),
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
