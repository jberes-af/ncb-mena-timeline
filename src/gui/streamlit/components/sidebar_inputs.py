# /src/gui/streamlit/components/sidebar_inputs.py

from src.application.dto.roi_use_case_dtos import CalculationInputsDTO
from src.domain.entities.entities import (
    EfficiencyAssumptions,
    FacilityProfile,
    IotPricingCatalog,
    IotSystemConfiguration,
    KitType,
)
from src.gui.streamlit.state.session_state import (
    get_roi_input_state,
    reset_roi_input_state,
    update_roi_input_state,
)

import streamlit as st


def get_kit_price(kit_type: KitType, catalog: IotPricingCatalog) -> float:
    prices: dict[KitType, float] = {
        KitType.ONE_PIECE: catalog.price_kit_one_piece,
        KitType.TWO_PIECE: catalog.price_kit__two_piece,
        KitType.THREE_PIECE: catalog.price_kit_three_piece,
        KitType.FOUR_PIECE: catalog.price_kit_four_piece,
    }

    return prices[kit_type]


def get_kit_label(kit_type: KitType, catalog: IotPricingCatalog) -> str:
    labels: dict[KitType, str] = {
        KitType.ONE_PIECE: (
            f"One-piece: Small Floor Mat "
            f"(${catalog.price_kit_one_piece:.2f})"
        ),
        KitType.TWO_PIECE: (
            f"Two-piece: Chair Pad + Small Floor Mat "
            f"(${catalog.price_kit__two_piece:.2f})"
        ),
        KitType.THREE_PIECE: (
            f"Three-piece: Chair Pad + Small & Large Floor Mats "
            f"(${catalog.price_kit_three_piece:.2f})"
        ),
        KitType.FOUR_PIECE: (
            f"Four-piece: Chair + Mattress Pads + Small & Large Floor Mats "
            f"(${catalog.price_kit_four_piece:.2f})"
        ),
    }

    return labels[kit_type]


def render_facility_inputs(state) -> tuple[int, int, float, float, float]:
    st.header("Facility Inputs")

    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        resident_count = st.number_input(
            "Residents",
            min_value=1,
            max_value=100,
            value=state.resident_count,
            key="resident_count_input",
        )

    with col_f2:
        caregiver_count = st.number_input(
            "Caregivers",
            min_value=1,
            max_value=50,
            value=state.caregiver_count,
            key="caregiver_count_input",
        )

    col_f3, col_f4 = st.columns([1, 1])

    with col_f3:
        loaded_wage = st.number_input(
            "Loaded Hourly Wage ($)",
            min_value=0.0,
            value=state.loaded_hourly_wage,
            key="loaded_wage_input",
        )

    with col_f4:
        pass

        """
        annual_payroll = st.number_input(
            "Annual caregiver payroll",
            value=state.annual_caregiver_payroll,
            key="annual_payroll_input",
        )
        """

    st.write("")
    st.write(f"Monthly Values per Resident:")

    col_f5, col_f6 = st.columns([1, 1])

    with col_f5:
        monthly_revenue = st.number_input(
            "Revenue",
            value=state.monthly_revenue_per_resident,
            key="monthly_revenue_input",
        )

    with col_f6:
        monthly_variable_cost = st.number_input(
            "Variable Cost",
            value=state.monthly_variable_cost_per_resident,
            key="monthly_variable_cost_input",
        )

    return (
        resident_count,
        caregiver_count,
        # annual_payroll,
        monthly_revenue,
        monthly_variable_cost,
        loaded_wage,
    )


def render_iot_system_inputs(
        state,
        catalog: IotPricingCatalog,
) -> tuple[KitType, float, int, int]:
    st.write("")
    st.header("Alerta Home Configuration")

    kit_type = st.selectbox(
        "Kit Type",
        options=list(KitType),
        format_func=lambda selected_kit: get_kit_label(selected_kit, catalog),
        key="kit_type",
        index=1,
    )

    kit_installations = st.number_input(
        "Kit Installations",
        min_value=1,
        max_value=50,
        value=state.kit_installations,
        key="kit_installations",
    )

    st.write("")
    st.write("Monthly Subscription")

    col_iot1, col_iot2 = st.columns([2, 1])

    with col_iot1:
        st.selectbox(
            label="Price ($)",
            options=(
                f"Monthly Subscription "
                f"(${catalog.price_monthly_subscription:.2f})",
            ),
            key="subscription_price",
            disabled=False,
            label_visibility="visible",
        )

    with col_iot2:
        contract_months = st.number_input(
            "Contract (months)",
            min_value=1,
            max_value=120,
            value=state.contract_months,
            key="contract_months_input",
        )

    """
    annual_discount_rate = st.slider(
        "Annual discount rate",
        min_value=0.0,
        max_value=0.30,
        value=state.annual_discount_rate,
        key="annual_discount_rate_input",
    )
    """

    selected_kit_price = get_kit_price(kit_type, catalog)

    return (
        kit_type,
        selected_kit_price,
        contract_months,
        # annual_discount_rate,
        kit_installations
    )


"""
def render_efficiency_inputs(state) -> tuple[float, float, float]:
    st.write("")
    st.header("Efficiency Assumptions")

    efficiency_gain = st.slider(
        "Caregiver efficiency gain",
        min_value=0.0,
        max_value=0.30,
        value=state.caregiver_efficiency_gain,
        key="efficiency_gain_input",
    )

    occupancy_lift = st.slider(
        "Occupancy lift, residents",
        min_value=0.0,
        max_value=5.0,
        value=state.occupancy_lift_residents,
        key="occupancy_lift_input",
    )

    overnight_hours_saved = st.slider(
        "Overnight hours saved per night",
        min_value=0.0,
        max_value=4.0,
        value=state.overnight_hours_saved_per_night,
        key="overnight_hours_saved_input",
    )

    return (
        efficiency_gain,
        occupancy_lift,
        overnight_hours_saved,
        # loaded_wage,
    )
"""


def render_efficiency_inputs(state) -> tuple[float, float, float, float, float, int, int]:
    st.write("")
    st.header("Efficiency Assumptions")

    gain_overnight_rounds = st.slider(
        "Time Saved Overnight Rounds (1 Shift) (minutes)",
        min_value=0,
        max_value=720,
        value=state.gain_overnight_rounds,
        key="gain_overnight_rounds",
        step=1,
    )

    gain_wellness_checks = st.slider(
        "Time Saved per Day (3 Shifts) - Wellness Checks (minutes)",
        min_value=0,
        max_value=720,
        value=state.gain_wellness_checks,
        key="gain_wellness_checks",
        step=1,
    )

    gain_documentation = st.slider(
        "Time Saved per Day (3 Shifts) - Documentation (minutes)",
        min_value=0,
        max_value=720,
        value=state.gain_documentation,
        key="gain_documentation",
        step=1,
    )

    gain_response_prioritization = st.slider(
        "Time Saved per Day (3 Shifts) - Response Prioritization (minutes)",
        min_value=0,
        max_value=720,
        value=state.gain_response_prioritization,
        key="gain_response_prioritization",
        step=1,
    )

    gain_room_entries = st.slider(
        "Time Saved per Day (3 Shifts) - Unnecessary Room Entries (minutes)",
        min_value=0,
        max_value=720,
        value=state.gain_room_entries,
        key="gain_room_entries",
        step=1,
    )

    st.write("")
    st.write("New Caregiver Hiring Delay")
    col_e1, col_e2 = st.columns([1, 1])

    with col_e1:
        months_hiring_delay = st.number_input(
            "Delay Period (months)",
            min_value=0,
            max_value=12,
            value=state.gain_hiring_delay,
            key="gain_hiring_delay",
        )

    with col_e2:
        count_positions_delayed = st.number_input(
            "Number of Positions",
            min_value=0,
            max_value=10,
            value=state.count_positioned_delayed,
            key="count_positioned_delayed",
        )

    return (
        gain_overnight_rounds,
        gain_wellness_checks,
        gain_documentation,
        gain_response_prioritization,
        gain_room_entries,
        months_hiring_delay,
        count_positions_delayed,
    )


def render_financial_calculation_assumptions(state) -> tuple[float]:
    st.write("")
    st.header("Financial Assumptions")

    annual_discount_rate = st.slider(
        "Annual Discount Rate",
        min_value=0.0,
        max_value=0.30,
        value=state.annual_discount_rate,
        key="annual_discount_rate_input",
    )

    return (
        annual_discount_rate,
    )


def render_reset_button() -> None:
    if st.button("Reset Assumptions"):
        reset_roi_input_state()
        st.rerun()


def get_calculation_inputs() -> CalculationInputsDTO:
    state = get_roi_input_state()
    catalog = IotPricingCatalog()

    with st.sidebar:
        (
            resident_count,
            caregiver_count,
            # annual_payroll,
            monthly_revenue,
            monthly_variable_cost,
            loaded_wage,
        ) = render_facility_inputs(state)

        (
            kit_type,
            selected_kit_price,
            contract_months,
            kit_installations,
            # annual_discount_rate,
        ) = render_iot_system_inputs(
            state=state,
            catalog=catalog,
        )

        (
            gain_overnight_rounds,
            gain_wellness_checks,
            gain_documentation,
            gain_response_prioritization,
            gain_room_entries,
            months_hiring_delay,
            count_positions_delayed,
        ) = render_efficiency_inputs(state)

        (
            annual_discount_rate,
        ) = render_financial_calculation_assumptions(state)

        render_reset_button()

    update_roi_input_state(
        resident_count=resident_count,
        caregiver_count=caregiver_count,
        # annual_caregiver_payroll=annual_payroll,
        monthly_revenue_per_resident=monthly_revenue,
        monthly_variable_cost_per_resident=monthly_variable_cost,
        subscription_price=catalog.price_monthly_subscription,
        contract_months=contract_months,
        annual_discount_rate=annual_discount_rate,
        gain_overnight_rounds=gain_overnight_rounds,
        gain_wellness_checks=gain_wellness_checks,
        gain_documentation=gain_documentation,
        gain_response_prioritization=gain_response_prioritization,
        gain_room_entries=gain_room_entries,
        loaded_hourly_wage=loaded_wage,
    )

    facility = FacilityProfile(
        resident_count=resident_count,
        caregiver_count=caregiver_count,
        # annual_caregiver_payroll=annual_payroll,
        monthly_revenue_per_resident=monthly_revenue,
        monthly_variable_cost_per_resident=monthly_variable_cost,
        loaded_hourly_wage=loaded_wage,
    )

    iot_system_config = IotSystemConfiguration(
        selected_kit_type=kit_type,
        selected_kit_price=selected_kit_price,
        monthly_subscription_price=catalog.price_monthly_subscription,
        contract_months=contract_months,
        annual_discount_rate=annual_discount_rate,
        kit_installations=kit_installations,
    )

    assumptions = EfficiencyAssumptions(
        gain_overnight_rounds=gain_overnight_rounds,
        gain_wellness_checks=gain_wellness_checks,
        gain_documentation=gain_documentation,
        gain_response_prioritization=gain_response_prioritization,
        gain_room_entries=gain_room_entries,
        hiring_delay_months=months_hiring_delay,
        count_positions_delayed=count_positions_delayed,
    )

    return CalculationInputsDTO(
        facility=facility,
        iot_system_config=iot_system_config,
        assumptions=assumptions,
    )
