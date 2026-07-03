# /src/gui/streamlit/auth/login_form.py

import streamlit as st

from src.interface_adapters.controllers.auth_controller import AuthController
from src.interface_adapters.presenters.auth_presenter import AuthPresenter


class LoginForm:
    def __init__(
        self,
        auth_controller: AuthController,
        auth_presenter: AuthPresenter,
    ) -> None:
        self.auth_controller = auth_controller
        self.auth_presenter = auth_presenter

    def render(self) -> None:
        st.write("Alerta Family: Mobile App Screen Flows")
        st.title("🔐 Sign in")

        email = st.text_input(
            "📧 Email Address",
            placeholder="you@example.com",
            key="auth_user_name",
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            key="auth_pwd",
        )

        submitted = st.button("✅ Login")

        if not submitted:
            return

        try:
            user = self.auth_controller.login(
                email=email,
                password=password,
            )

            view_model = self.auth_presenter.present_success(user)

        except Exception as exc:
            view_model = self.auth_presenter.present_error(exc)

        if not view_model.success:
            st.error(view_model.message)
            return

        st.session_state["logged_in"] = True
        st.session_state["user"] = {
            "email": view_model.user.email,
            "uid": view_model.user.uid,
            "name": view_model.user.display_name,
        }

        st.success(view_model.message)
        st.rerun()
