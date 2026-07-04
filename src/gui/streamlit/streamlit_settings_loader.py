# /src/gui/streamlit/streamlit_settings_loader.py

from src.infrastructure.config.secret_provider import SecretProvider


class StreamlitSecretProvider(SecretProvider):
    def get(
        self,
        name: str,
        default: str | None = None,
    ) -> str | None:
        import streamlit as st

        value = st.secrets.get(name, default)

        if value is None:
            return None

        return str(value).strip()