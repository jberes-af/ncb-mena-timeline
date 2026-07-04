# infrastructure/google/auth/google_credentials_provider.py

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

@dataclass(frozen=True)
class OAuthTokenCredentialsProvider:
    token_json: Path
    scopes: Sequence[str]

    def load(self) -> Credentials:
        if not self.token_json.exists():
            raise FileNotFoundError(
                f"Missing token file: {self.token_json}. "
                "Run your dev bootstrap OAuth script to generate token.json."
            )

        creds = Credentials.from_authorized_user_file(str(self.token_json), list(self.scopes))

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Persist refreshed token
            self.token_json.write_text(creds.to_json(), encoding="utf-8")

        if not creds.valid:
            raise RuntimeError("Google credentials are invalid and could not be refreshed.")

        granted = set(creds.scopes or [])
        required = set(self.scopes)
        missing = required - granted
        if missing:
            raise RuntimeError(
                "OAuth token is missing required scopes. "
                "Regenerate token with the updated scope set. "
                f"Missing: {sorted(missing)}"
            )

        return creds
