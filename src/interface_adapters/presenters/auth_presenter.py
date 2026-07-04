# /src/interface_adapters/presenters/auth_presenter.py

from dataclasses import dataclass
from src.application.auth.dto import AuthenticatedUserDTO


@dataclass(frozen=True)
class AuthViewModel:
    success: bool
    message: str
    user: AuthenticatedUserDTO | None = None


class AuthPresenter:
    def present_success(self, user: AuthenticatedUserDTO) -> AuthViewModel:
        return AuthViewModel(
            success=True,
            message=f"Welcome back, {user.email}!",
            user=user,
        )

    def present_error(self, message: str) -> AuthViewModel:
        return AuthViewModel(
            success=False,
            message=message,
        )
