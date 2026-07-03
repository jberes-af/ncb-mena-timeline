# /src/gui/streamlit/state/session_state.py

from dataclasses import asdict

from src.gui.streamlit.state.state_models import RoiInputState

import streamlit as st

ROI_INPUT_STATE_KEY = "roi_input_state"


def get_roi_input_state() -> RoiInputState:
    default_state = RoiInputState()

    if ROI_INPUT_STATE_KEY not in st.session_state:
        st.session_state[ROI_INPUT_STATE_KEY] = default_state
        return st.session_state[ROI_INPUT_STATE_KEY]

    current_state = st.session_state[ROI_INPUT_STATE_KEY]

    # Add any newly introduced fields automatically
    for field_name, default_value in asdict(default_state).items():
        if not hasattr(current_state, field_name):
            setattr(current_state, field_name, default_value)

    return current_state


def update_roi_input_state(**kwargs) -> RoiInputState:
    state = get_roi_input_state()

    for key, value in kwargs.items():
        if hasattr(state, key):
            setattr(state, key, value)

    return state


def reset_roi_input_state() -> None:
    st.session_state[ROI_INPUT_STATE_KEY] = RoiInputState()
