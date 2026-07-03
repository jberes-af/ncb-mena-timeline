# /src/gui/streamlit/app.py

from src.application.dto.roi_use_case_dtos import CalculationInputsDTO

from src.application.use_cases.use_cases import CalculateRoiUseCase

from src.gui.streamlit.components.sidebar_inputs import get_calculation_inputs
from src.gui.streamlit.screens.roi_calculation_page import render_roi_calculation_screen

from src.application.services.calculate_operator_benefits import (
    OperatorBenefitsCalculator)

import streamlit as st


def run_app() -> None:
    st.set_page_config(page_title="Alerta Home ROI Calculator", layout="wide")

    calculation_inputs: CalculationInputsDTO = get_calculation_inputs()

    run_calculate_roi_use_case = CalculateRoiUseCase(
        calculate_benefits=OperatorBenefitsCalculator(),
    )

    result = run_calculate_roi_use_case.execute(
        facility=calculation_inputs.facility,
        iot_system_config=calculation_inputs.iot_system_config,
        assumptions=calculation_inputs.assumptions,
    )

    render_roi_calculation_screen(result=result)


if __name__ == "__main__":
    run_app()
