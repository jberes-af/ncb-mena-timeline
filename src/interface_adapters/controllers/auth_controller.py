# /src/interface_adapters/controllers/auth_controller.py

from src.application.auth.dto import LoginRequestDTO
from src.application.auth.login_user import LoginUser


class AuthController:
    def __init__(self, login_user: LoginUser):
        self.login_user = login_user

    def login(self, email: str, password: str):
        request = LoginRequestDTO(email=email, password=password)
        return self.login_user.execute(request)
