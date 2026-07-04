# /src/application/firebase_auth/login_user.py

from src.application.auth.dto import LoginRequestDTO, AuthenticatedUserDTO
from src.application.auth.ports import AuthProvider


class LoginUser:
    def __init__(self, auth_provider: AuthProvider):
        self.auth_provider = auth_provider

    def execute(self, request: LoginRequestDTO) -> AuthenticatedUserDTO:
        if not request.email or not request.password:
            raise ValueError("Email and password are required.")

        return self.auth_provider.authenticate(
            email=request.email,
            password=request.password,
        )
