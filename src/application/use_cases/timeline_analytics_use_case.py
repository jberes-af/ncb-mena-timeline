# /src/application/use_cases/timeline_analytics_use_case.py

from collections import Counter

from src.application.dto.show_timeline_dtos import TimelineEventViewDTO
from src.application.dto.analytics_dtos import (
    EntityReferenceCountDTO,
    TimelineAnalyticsResultDTO,
)


class TimelineAnalyticsUseCase:
    def execute(
            self,
            *,
            selected_country_ids: tuple[str, ...],
            selected_actor_ids: tuple[str, ...],
            timeline_events: tuple[TimelineEventViewDTO, ...],
    ) -> TimelineAnalyticsResultDTO:
        if not timeline_events:
            return TimelineAnalyticsResultDTO(
                count_selected_countries=len(selected_country_ids),
                count_actors_selected=len(selected_actor_ids),
                count_actors_involved=0,
                entity_reference_counts=(),
                count_events=0,
                count_years_in_timeline=0,
                first_year=None,
                last_year=None,
                year_range=0,
                count_citations=0,
            )

        years = {event.year for event in timeline_events}
        first_year = min(years)
        last_year = max(years)

        citations = {
            citation.citation_id
            for event in timeline_events
            for citation in event.citations
        }

        entity_reference_counter: Counter[str] = Counter(
            reference
            for event in timeline_events
            for reference in event.country_abbreviations
        )

        entity_reference_counts = tuple(
            EntityReferenceCountDTO(
                entity_reference=reference,
                count=count,
            )
            for reference, count in sorted(
                entity_reference_counter.items(),
                key=lambda item: (-item[1], item[0]),
            )
        )

        return TimelineAnalyticsResultDTO(
            count_selected_countries=len(selected_country_ids),
            count_actors_selected=len(selected_actor_ids),
            count_actors_involved=len(entity_reference_counts),
            entity_reference_counts=entity_reference_counts,
            count_events=len(timeline_events),
            count_years_in_timeline=len(years),
            first_year=first_year,
            last_year=last_year,
            year_range=last_year - first_year + 1,
            count_citations=len(citations),
        )
