# /src/gui/streamlit/components/sidebar_inputs.py

from dataclasses import dataclass

from src.domain.entities.entities import (
    ActorRecordDTO,
    CountryRecordDTO,
    TimelineInputsDTO,
)

import streamlit as st


@dataclass(frozen=True)
class UserSidebarSelections:
    selected_country_ids: tuple[str, ...]
    selected_actor_ids: tuple[str, ...]
    selected_years: tuple[int, ...]
    run_clicked: bool


def render_country_checkbox_list(
        *,
        countries: tuple[CountryRecordDTO, ...],
) -> tuple[str, ...]:
    selected_country_ids: list[str] = []

    sorted_countries = sorted(
        countries,
        key=lambda country: country.country_name,
    )

    st.write("Countries")

    for country in sorted_countries:

        col_checkbox, col_label = st.columns([1, 8])

        with col_checkbox:
            is_selected = st.checkbox(
                label=f"Select {country.country_name}",
                key=f"country_checkbox_{country.country_id}",
                label_visibility="collapsed",
            )

        with col_label:
            st.markdown(
                f"""
                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                    min-height:30px;
                    margin-top:5px;
                ">
                    <img
                        src="{_flag_url(country.abbreviation_2)}"
                        width="28"
                    />
                    <span>
                        {country.country_name}
                        ({country.abbreviation_3})
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if is_selected:
            selected_country_ids.append(country.country_id)

    return tuple(selected_country_ids)


def render_non_country_actor_checkbox_list(
        *,
        actors: tuple[ActorRecordDTO, ...],
) -> tuple[str, ...]:
    selected_actor_ids: list[str] = []

    sorted_actors = sorted(
        actors,
        key=lambda actor: actor.actor_name,
    )

    st.write("Actors")

    for actor in sorted_actors:

        col_checkbox, col_label = st.columns([1, 8])

        with col_checkbox:
            is_selected = st.checkbox(
                label=f"Select {actor.actor_name}",
                key=f"actor_checkbox_{actor.actor_id}",
                label_visibility="collapsed",
            )

        with col_label:
            st.markdown(
                f"""
                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                    min-height:30px;
                    margin-top:5px;
                ">
                    <span>
                        {actor.actor_name} ({actor.actor_reference})
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if is_selected:
            selected_actor_ids.append(actor.actor_id)

    return tuple(selected_actor_ids)


def render_year_checkbox_list(
        *,
        timeline_inputs: TimelineInputsDTO,
) -> tuple[int, ...]:
    selected_years: list[int] = []

    years = sorted(
        {event.year for event in timeline_inputs.events}
    )

    st.write("Years")

    for year in years:
        is_selected = st.checkbox(
            label=str(year),
            key=f"year_checkbox_{year}",
            value=True,
        )

        if is_selected:
            selected_years.append(year)

    return tuple(selected_years)


def load_sidebar_inputs(
        *,
        timeline_inputs: TimelineInputsDTO,
) -> UserSidebarSelections:
    with st.sidebar:
        st.header("Timeline Filters")

        selected_country_ids = render_country_checkbox_list(
            countries=timeline_inputs.country_records,
        )

        st.divider()

        selected_actor_ids = render_non_country_actor_checkbox_list(
            actors=tuple(
                actor
                for actor in timeline_inputs.actor_records
                if not actor.is_country
            ),
        )

        # st.divider()
        # selected_years = render_year_checkbox_list(timeline_inputs=timeline_inputs)
        selected_years: list[int] = sorted(
            {int(event.year) for event in timeline_inputs.events}
        )

        st.divider()

        run_clicked = st.button(
            "Show Timeline",
            type="primary",
            use_container_width=True,
        )

    return UserSidebarSelections(
        selected_country_ids=selected_country_ids,
        selected_actor_ids=selected_actor_ids,
        selected_years=tuple(selected_years),
        run_clicked=run_clicked,
    )


def _flag_url(abbreviation_2: str) -> str:
    return f"https://flagcdn.com/w80/{abbreviation_2.strip().lower()}.png"
