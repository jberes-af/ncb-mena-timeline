# /src/gui/streamlit/screens/timeline_page.py
# /src/gui/streamlit/screens/timeline_page.py

from html import escape
import calendar

import streamlit as st

from src.application.dto.show_timeline_dtos import (
    ShowTimelineResultDTO,
)


def render_timeline_screen(
    *,
    result: ShowTimelineResultDTO,
) -> None:
    st.header("Timeline")

    if not result.events:
        st.info("No events found for the selected countries and years.")
        return

    current_year: int | None = None

    for event in result.events:
        if event.year != current_year:
            current_year = event.year
            st.markdown(f"## {event.year}")

        flag_images: str = _render_flag_images(event.country_alpha2_codes)
        description: str = escape(event.event_description)
        citations: str = escape(", ".join(event.citation_ids))
        date_label: str = _format_date_label(month=event.month)

        _render_event_card(
            flag_images=flag_images,
            description=description,
            citations=citations,
            date_label=date_label,
        )


def _render_event_card(
    *,
    flag_images: str,
    description: str,
    citations: str,
    date_label: str,
) -> None:
    st.html(
        f"""
        <div style="
            background:#fafafa;
            border-radius:8px;
            padding:12px 16px;
            margin-bottom:12px;
            border-left:4px solid #cccccc;
        ">
            <div style="
                font-size:13px;
                color:#777777;
                margin-bottom:6px;
            ">
                {date_label}
            </div>

            <div style="
                display:flex;
                align-items:center;
                gap:8px;
                margin-bottom:10px;
            ">
                {flag_images}
            </div>

            <div style="
                font-size:16px;
                line-height:1.45;
                margin-top:4px;
            ">
                {description}
            </div>

            <div style="
                font-size:13px;
                color:#666666;
                margin-top:8px;
            ">
                Citations: {citations}
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
