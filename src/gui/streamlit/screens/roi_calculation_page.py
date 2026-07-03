# /src/gui/streamlit/screens/roi_calculation_page.py


from src.application.dto.roi_use_case_dtos import CalculateRoiResultDTO

import streamlit as st


def _format_currency(value: float) -> str:
    return f"${value:,.0f}"


def _format_percent(value: float) -> str:
    return f"{value:.0%}"


def _format_payback_months(value: float | None) -> str:
    if value is None:
        return "N/A"

    return f"{value:.1f}"


def render_summary_metrics(result: CalculateRoiResultDTO) -> None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Annualized Net Benefit",
        _format_currency(result.net_annual_benefit),
    )

    col2.metric(
        "Annualized Alerta Home Price",
        _format_currency(result.annualized_iot_cost),
    )

    col3.metric(
        "Gross Payback (months)",
        _format_payback_months(result.payback_months),
    )

    col4.metric(
        "Net ROI",
        _format_percent(result.roi_percent),
    )


def render_operator_benefit_section(result: CalculateRoiResultDTO) -> None:
    st.subheader("Financial Return")

    st.write("**Operator Benefit**")
    st.write(
        f"Caregiver staff payroll, annual: "
        f"**{_format_currency(result.staff_payroll_annual)}**"
    )
    st.write(
        f"Efficiency contributions from Alerta Home, annual: "
        f"**{_format_currency(result.efficiency_total)}**"
    )
    st.write(
        f"Operational efficiency from Alerta Home: "
        f"**{100 * result.iot_percent_efficiency:.1f}%**"
    )
    st.write(
        f"Theoretical added resident capacity: "
        f"**{result.added_residents_theoretical:.1f} residents**"
    )
    st.write(
        f"Applied added resident capacity: "
        f"**{result.added_residents_use_case:.1f} residents**"
    )


def render_new_resident_value_section(result: CalculateRoiResultDTO) -> None:
    st.write("")
    st.write("**New Resident Added Value**")

    st.write(
        f"New resident added value, theoretical annual: "
        f"**{_format_currency(result.new_resident_value_theoretical)}**"
    )

    st.write(
        f"New resident added value, applied monthly: "
        f"**{_format_currency(result.new_resident_value_use_case)}**"
    )

    st.write(
        f"New resident added value, applied annualized: "
        f"**{_format_currency(result.new_resident_value_use_case * 12)}**"
    )


def render_iot_cost_section(result: CalculateRoiResultDTO) -> None:
    st.write("")
    st.write("**Alerta Home Cost Inputs**")

    st.write(f"Hardware cost: **{_format_currency(result.hardware_cost)}**")
    st.write(
        f"Monthly subscription cost: "
        f"**{_format_currency(result.monthly_subscription_cost)}**"
    )
    st.write(
        f"Subscription term: "
        f"**{result.contract_term_months:,.0f} months**"
    )

    st.write("")
    st.write("**Discounted Cost Summary**")
    st.write(f"NPV of system cost: **{_format_currency(result.npv_iot_cost)}**")
    st.write(
        f"Monthly equivalent system cost: "
        f"**{_format_currency(result.monthly_iot_cost)}**"
    )
    st.write(
        f"Annualized equivalent system cost: "
        f"**{_format_currency(result.annualized_iot_cost)}**"
    )


def render_net_benefit_section(result: CalculateRoiResultDTO) -> None:
    st.write("")
    st.write("**Net Financial Output**")
    st.write(
        f"Annualized net benefit: "
        f"**{_format_currency(result.net_annual_benefit)}**"
    )
    st.write(
        f"Monthly equivalent net benefit: "
        f"**{_format_currency(result.net_annual_benefit / 12)}**"
    )
    st.write(
        f"Gross payback period: "
        f"**{_format_payback_months(result.payback_months)} months**"
    )
    st.write(f"Net ROI: **{_format_percent(result.roi_percent)}**")


def render_efficiency_components_table(result: CalculateRoiResultDTO) -> None:
    st.subheader("Efficiency Components, Annualized")

    st.table(
        {
            "Component": [
                "Reduced overnight rounds time",
                "Reduced wellness check time",
                "Reduced documentation time",
                "Reduced response prioritization time",
                "Reduced unnecessary room entry time",
                "Delayed new caregiver hiring",
                "Total",
            ],
            "Annual Value": [
                _format_currency(result.efficiency_overnight_rounds),
                _format_currency(result.efficiency_wellness_checks),
                _format_currency(result.efficiency_documents),
                _format_currency(result.efficiency_prioritization),
                _format_currency(result.efficiency_room_entries),
                _format_currency(result.delayed_hiring_value),
                _format_currency(result.efficiency_total),
            ],
        }
    )


def render_roi_calculation_screen(result: CalculateRoiResultDTO) -> None:
    st.title("Care Facility Alerta Home ROI Calculator")

    render_summary_metrics(result)

    st.write("")
    render_operator_benefit_section(result)

    render_new_resident_value_section(result)

    render_iot_cost_section(result)

    render_net_benefit_section(result)

    st.write("")
    render_efficiency_components_table(result)

