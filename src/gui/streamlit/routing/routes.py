# /src/gui/streamlit/routing/routes.py

from src.gui.streamlit.routing.route_types import RouteHandler

from src.gui.streamlit.screens.timeline_page import render_timeline_screen


NAVIGATION: dict[str, dict[str, RouteHandler]] = {
    "Overview": {
       "Mobile App Overview": render_timeline_screen,
    },
}
