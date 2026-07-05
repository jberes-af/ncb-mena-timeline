# /src/gui/streamlit/app.py

from pathlib import Path  # local file system only

from src.application.dto.timeline_analytics_dtos import TimelineAnalyticsResultDTO
from src.domain.entities.entities import TimelineInputsDTO

from src.application.dto.show_timeline_dtos import (
    ShowTimelineRequestDTO,
    ShowTimelineResultDTO,
)

from src.application.dto.dataset_analytics_dtos import (
    DatasetAnalyticsResultDTO,
)

from src.application.use_cases.show_timeline_use_case import (
    ShowTimelineUseCase)

from src.application.use_cases.timeline_analytics_use_case import (
    TimelineAnalyticsUseCase)

from src.application.use_cases.dataset_analytics_use_case import (
    DatasetAnalyticsUseCase,
)

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


def run_use_case_dataset_analytics(
        timeline_inputs: TimelineInputsDTO,
        project_root: Path,
) -> DatasetAnalyticsResultDTO:
    dataset_analytics_result: DatasetAnalyticsResultDTO = (
        DatasetAnalyticsUseCase().execute(
            timeline_inputs=timeline_inputs,
            project_root=project_root
        ))

    return dataset_analytics_result


def _run_use_case_actor_relationships_analytics(
        timeline_inputs: TimelineInputsDTO,
):
    pass


def run_use_cases_timeline(
        timeline_inputs: TimelineInputsDTO,
        selected_country_ids: tuple[str, ...],
        selected_actor_ids: tuple[str, ...],
        selected_years: tuple[int, ...],
) -> tuple[ShowTimelineResultDTO, TimelineAnalyticsResultDTO]:
    show_timeline_use_case = ShowTimelineUseCase()

    timeline_events_result: ShowTimelineResultDTO = (
        show_timeline_use_case.execute(
            ShowTimelineRequestDTO(
                timeline_inputs=timeline_inputs,
                selected_country_ids=selected_country_ids,
                selected_actor_ids=selected_actor_ids,
                selected_years=selected_years,
            )
        ))

    timeline_analytics_use_case = TimelineAnalyticsUseCase()

    timeline_analytics_result: TimelineAnalyticsResultDTO = (
        timeline_analytics_use_case.execute(
            selected_country_ids=selected_country_ids,
            selected_actor_ids=selected_actor_ids,
            timeline_events=timeline_events_result.events,
        ))

    return timeline_events_result, timeline_analytics_result


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

    # --- RUN DATASET ANALYTICS

    dataset_analytics_result: DatasetAnalyticsResultDTO = (
        run_use_case_dataset_analytics(
            timeline_inputs=timeline_inputs,
            project_root=app_container.settings.project_root
        ))

    # _run_use_case_actor_relationships_analytics(
    # timeline_inputs=timeline_inputs,)

    # -- RUN USER-SELECTED TIMELINE ANALYSES

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

    timeline_results: tuple[ShowTimelineResultDTO, TimelineAnalyticsResultDTO] = (
        run_use_cases_timeline(
            timeline_inputs=timeline_inputs,
            selected_country_ids=sidebar_inputs.selected_country_ids,
            selected_actor_ids=sidebar_inputs.selected_actor_ids,
            selected_years=sidebar_inputs.selected_years,
        ))

    timeline_events_result: ShowTimelineResultDTO = timeline_results[0]
    timeline_analytics_result: TimelineAnalyticsResultDTO = timeline_results[1]

    # --- RENDER STREAMLIE

    render_timeline_screen(
        timeline_events=timeline_events_result,
        timeline_analytics=timeline_analytics_result,
        dataset_analytics=dataset_analytics_result,
    )


if __name__ == "__main__":
    run_app()
