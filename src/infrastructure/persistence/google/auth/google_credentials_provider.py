# infrastructure/google/auth/google_credentials_provider.py

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


@dataclass(frozen=True)
class OAuthTokenCredentialsProvider:
    token_json: Path | dict[str, Any]
    scopes: Sequence[str]

    def load(self) -> Credentials:

        # ---------- Streamlit / secrets ----------
        if isinstance(self.token_json, dict):
            creds = Credentials.from_authorized_user_info(
                self.token_json,
                scopes=list(self.scopes),
            )

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())

            return creds

        # ---------- Local development ----------
        if not self.token_json.exists():
            raise FileNotFoundError(
                f"Missing token file: {self.token_json}"
            )

        creds = Credentials.from_authorized_user_file(
            str(self.token_json),
            scopes=list(self.scopes),
        )

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

            # Persist refreshed token locally
            self.token_json.write_text(
                creds.to_json(),
                encoding="utf-8",
            )

        if not creds.valid:
            raise RuntimeError(
                "Google credentials are invalid and could not be refreshed."
            )

        granted = set(creds.scopes or [])
        required = set(self.scopes)

        missing = required - granted

        if missing:
            raise RuntimeError(
                "OAuth token is missing required scopes. "
                f"Missing: {sorted(missing)}"
            )

        return creds