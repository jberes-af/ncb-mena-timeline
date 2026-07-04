# /src/gui/streamlit/app.py

from src.domain.entities.entities import TimelineInputsDTO

from src.application.dto.show_timeline_dtos import ShowTimelineRequestDTO

from src.application.use_cases.show_timeline_use_case import (
    ShowTimelineUseCase)

from src.application.use_cases.timeline_analytics_use_case import (
    TimelineAnalyticsUseCase)

from src.gui.streamlit.components.sidebar_inputs import (
    load_sidebar_inputs,
    UserSidebarSelections,
)

from src.gui.streamlit.screens.timeline_page import render_timeline_screen

from src.main.composition_root import app_container

import streamlit as st


@st.cache_data(show_spinner="Loading Google Sheets data...")
def load_timeline_inputs() -> TimelineInputsDTO:
    return app_container.timeline_inputs_repository.load_timeline_inputs()


def run_app() -> None:
    st.set_page_config(
        page_title="MENA Timeline Project",
        layout="wide",
    )

    st.title("MENA Timeline Project")

    col_1, col_2 = st.columns([2, 4])

    with col_1:

        run_clicked_2: bool = st.button(
            "Show Timeline",
            type="primary",
            use_container_width=True,
        )

    timeline_inputs: TimelineInputsDTO = load_timeline_inputs()

    sidebar_inputs: UserSidebarSelections = load_sidebar_inputs(
        timeline_inputs=timeline_inputs,
    )

    run_clicked: bool = sidebar_inputs.run_clicked or run_clicked_2

    if not run_clicked:
        st.info("Select countries and years, then click `Show Timeline`.")
        return

    if not sidebar_inputs.selected_country_ids and not sidebar_inputs.selected_actor_ids:
        st.warning("Please select at least one country or non-country actor.")
        return

    # if not sidebar_inputs.selected_years:
        # st.warning("Please select at least one year.")
        # return

    show_timeline_use_case = ShowTimelineUseCase()

    timeline_result = show_timeline_use_case.execute(
        ShowTimelineRequestDTO(
            timeline_inputs=timeline_inputs,
            selected_country_ids=sidebar_inputs.selected_country_ids,
            selected_actor_ids=sidebar_inputs.selected_actor_ids,
            selected_years=sidebar_inputs.selected_years,
        )
    )

    analytics_result = TimelineAnalyticsUseCase().execute(
        selected_country_ids=sidebar_inputs.selected_country_ids,
        selected_actor_ids=sidebar_inputs.selected_actor_ids,
        timeline_events=timeline_result.events,
    )

    render_timeline_screen(
        result=timeline_result,
        analytics=analytics_result,
    )


if __name__ == "__main__":
    run_app()
