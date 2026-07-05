# /src/gui/streamlit/screens/timeline_page.py

from html import escape

from src.application.dto.dataset_analytics_dtos import DatasetAnalyticsResultDTO
from src.application.dto.show_timeline_dtos import ShowTimelineResultDTO

from src.application.dto.timeline_analytics_dtos import TimelineAnalyticsResultDTO

from src.gui.streamlit.screens.timeline_page_relationships_chart import (
    render_actor_pair_counts_chart,
)

import calendar
import streamlit as st


def render_timeline_screen(
        *,
        timeline_events: ShowTimelineResultDTO,
        timeline_analytics: TimelineAnalyticsResultDTO | None = None,
        dataset_analytics: DatasetAnalyticsResultDTO | None = None,
) -> None:
    st.header("Entity Relationships")

    render_actor_pair_counts_chart(
        pair_counts=dataset_analytics.pair_counts,
        max_pairs=10,
    )

    st.write("")

    st.header("Timeline Selections Summary")

    if timeline_analytics is not None:
        _render_timeline_analytics(timeline_analytics)

    st.write("")

    st.header("Timeline Events")

    if not timeline_events.events:
        st.info("No events found for the selected countries and years.")
        return

    current_year: int | None = None

    for event in timeline_events.events:
        if event.year != current_year:
            current_year = event.year
            st.markdown(f"## {event.year}")

        _render_event_card(
            flag_images=_render_flag_images(event.country_alpha2_codes),
            description=escape(event.event_description),
            date_label=_format_date_label(month=event.month),
        )

        _render_event_citations(event.citations)


def _render_event_card(
        *,
        flag_images: str,
        description: str,
        date_label: str,
) -> None:
    st.html(
        f"""
        <div style="
            background:#fafafa;
            border-radius:8px;
            padding:12px 16px;
            margin-bottom:6px;
            border-left:4px solid #cccccc;
        ">
            <div style="font-size:13px;color:#777777;margin-bottom:6px;">
                {date_label}
            </div>

            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                {flag_images}
            </div>

            <div style="font-size:16px;line-height:1.45;margin-top:4px;">
                {description}
            </div>
        </div>
        """
    )


def _render_flag_images(
        alpha2_codes: tuple[str, ...],
) -> str:
    return "".join(
        f"""
        <img
            src="https://flagcdn.com/w40/{alpha2.strip().lower()}.png"
            width="28"
            style="margin-right:8px; vertical-align:middle;"
        />
        """
        for alpha2 in alpha2_codes
        if alpha2 and len(alpha2.strip()) == 2
    )


def _format_date_label(
        *,
        month: int | None,
) -> str:
    if month is None:
        return ""

    return calendar.month_name[month]


def _render_event_citations(
        citations,
) -> None:
    if not citations:
        return

    with st.expander(f"Sources ({len(citations)})"):
        for citation in citations:
            st.markdown(
                f"""
                **{escape(citation.citation_id)}**  
                {escape(citation.citation_text)}
                """
            )


def _render_timeline_analytics(
        analytics: TimelineAnalyticsResultDTO,
) -> None:
    with st.expander("Analytics", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Events", analytics.count_events)
            st.metric("Years with Events", analytics.count_years_in_timeline)

        with col2:
            st.metric("Countries Selected", analytics.count_selected_countries)
            st.metric("Actors Selected", analytics.count_actors_selected)

        with col3:
            st.metric("Entities Involved", analytics.count_actors_involved)
            st.metric("Citations", analytics.count_citations)

        if analytics.first_year is not None and analytics.last_year is not None:
            st.write(
                f"Time Range: **{analytics.first_year}–{analytics.last_year}** "
                f"({analytics.year_range} years)"
            )

        """
        if analytics.entity_reference_counts:
            st.write("Entities involved:")
            st.write("  •  ".join(analytics.entity_reference_counts))
        """

        if analytics.entity_reference_counts:
            st.write("Entity counts:")

            for item in analytics.entity_reference_counts:
                st.markdown(
                    f"- **{escape(item.entity_reference)}**: {item.count}"
                )

        """
        if analytics.entity_reference_counts:
            st.write("Entity counts:")

            st.dataframe(
                [
                    {
                        "Entity": item.entity_reference,
                        "Events": item.count,
                    }
                    for item in analytics.entity_reference_counts
                ],
                use_container_width=True,
                hide_index=True,
            )
        """
