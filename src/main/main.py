# src/main.py

"""
main.py is used ONLY if there is use case beyond the streamlit app
"""

# from src.gui.streamlit.app import run_streamlit_app


import logging
from sys import stderr
import traceback

from src.main.composition_root import app_container


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main() -> int:
    configure_logging()

    try:
        # For this Streamlit app, main.py does not launch the UI.
        # It only verifies that the application can be composed.
        logging.info("App container built successfully")
        logging.info("Config path: %s", app_container.settings.config_path)
        return 0

    except ValueError as exc:
        print(f"ERROR (User / Validation): {exc}", file=stderr)
        traceback.print_exc()
        return 2

    except Exception:
        print("UNHANDLED ERROR (Internal):", file=stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
