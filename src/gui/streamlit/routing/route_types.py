# /src/gui/streamlit/routing/route_types.py

from collections.abc import Callable

RouteHandler = Callable[[], None]
