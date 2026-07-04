# /src/application/firebase_auth/dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class LoginRequestDTO:
    email: str
    password: str


@dataclass(frozen=True)
class AuthenticatedUserDTO:
    email: str
    uid: str
    id_token: str = ""
    refresh_token: str = ""
    display_name: str = ""