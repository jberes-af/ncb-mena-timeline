# /src/infrastructure/config/secret_provider.py

from abc import ABC, abstractmethod
from pathlib import Path
import os

from dotenv import load_dotenv


class SecretProvider(ABC):
    @abstractmethod
    def get(self, name: str, default: str | None = None) -> str | None:
        raise NotImplementedError

    def get_required(self, name: str) -> str:
        value = self.get(name)

        if value is None or not value.strip():
            raise RuntimeError(f"Missing required secret: {name}")

        return value.strip()


class StreamlitSecretProvider(SecretProvider):
    def get(
        self,
        name: str,
        default: str | None = None,
    ) -> str | None:
        import streamlit as st

        value = st.secrets.get(name, default)
        return str(value).strip() if value else value


class EnvSecretProvider(SecretProvider):
    def __init__(self, env_path: Path | None = None) -> None:

        if env_path is not None:
            load_dotenv(env_path)

    def get(self, name: str, default: str | None = None) -> str | None:
        value = os.getenv(name, default)
        return value.strip() if value else value
