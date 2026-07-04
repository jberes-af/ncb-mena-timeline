# /src/gui/streamlit/app.py
# /src/gui/streamlit/app.py

import streamlit as st

from src.application.dto.show_timeline_dtos import ShowTimelineRequestDTO
from src.application.use_cases.show_timeline_use_case import ShowTimelineUseCase
from src.gui.streamlit.components.sidebar_inputs import load_sidebar_inputs
from src.gui.streamlit.screens.timeline_page import render_timeline_screen
from src.main.composition_root import app_container


@st.cache_data(show_spinner="Loading Google Sheets data...")
def load_timeline_inputs():
    return app_container.timeline_inputs_repository.load_timeline_inputs()


def run_app() -> None:
    st.set_page_config(
        page_title="MENA Timeline Project",
        layout="wide",
    )

    st.title("MENA Timeline Project")

    col_1, col_2 = st.columns([2, 4])

    with col_1:

        run_clicked_2 = st.button(
            "Show Timeline",
            type="primary",
            use_container_width=True,
        )

    timeline_inputs = load_timeline_inputs()

    selected_country_ids, selected_years, run_clicked = load_sidebar_inputs(
        timeline_inputs=timeline_inputs,
    )

    if not run_clicked and not run_clicked_2:
        st.info("Select countries and years, then click `Show Timeline`.")
        return

    if not selected_country_ids:
        st.warning("Please select at least one country.")
        return

    if not selected_years:
        st.warning("Please select at least one year.")
        return

    use_case = ShowTimelineUseCase()

    result = use_case.execute(
        ShowTimelineRequestDTO(
            timeline_inputs=timeline_inputs,
            selected_country_ids=selected_country_ids,
            selected_years=selected_years,
        )
    )

    render_timeline_screen(result=result)


if __name__ == "__main__":
    run_app()
