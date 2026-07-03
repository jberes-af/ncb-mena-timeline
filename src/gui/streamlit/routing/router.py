# /src/gui/streamlit/routing/router.py

from typing import Any

from src.gui.streamlit.routing.route_types import RouteHandler
from src.gui.streamlit.routing.routes import NAVIGATION

import streamlit as st

DEFAULT_SECTION = "Overview"


def get_selected_route() -> tuple[str, str]:
    sections = list(NAVIGATION.keys())

    selected_section: Any = st.sidebar.radio(
        label="Navigation Group",
        options=sections,
        index=sections.index(DEFAULT_SECTION),
        key="selected_navigation_group",
    )

    route_names = list(NAVIGATION[selected_section].keys())

    selected_route: Any = st.sidebar.radio(
        label="Page",
        options=route_names,
        key=f"selected_route_{selected_section}",
    )

    return selected_section, selected_route


def render_route(section_name: str, route_name: str) -> None:
    route_handler: RouteHandler | None = NAVIGATION.get(section_name, {}).get(route_name)

    if route_handler is None:
        st.error(f"Unknown route: {section_name} / {route_name}")
        return

    route_handler()


def render_router() -> None:
    section_name, route_name = get_selected_route()
    render_route(section_name, route_name)

