# /application/ports/google_credentials_provider_port.py

from typing import Protocol
from google.auth.credentials import Credentials


class GoogleCredentialsProviderPort(Protocol):
    def load(self) -> Credentials:
        ...
