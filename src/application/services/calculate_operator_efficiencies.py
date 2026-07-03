# /src/application/services/calculate_operator_efficiencies.py

from src.application.dto.roi_use_case_dtos import OperatorBenefitsDTO

from src.domain.services.operator_calculations import (
    contribution_margin,
    added_capacity,
)

HOURS_PER_MINUTE: float = 1 / 60
DAYS_PER_YEAR: int = 365
HOURS_PER_MONTH_1_FTE: float = 2080  / 12  # 40 hours p week * 52 weeks per year


def calculate_annual_gain_overnight_rounds(
        loaded_wage: float,  # hourly wage
        gain_overnight_rounds_minutes: float,

) -> float:
    gain_hours_p_day: float = gain_overnight_rounds_minutes * HOURS_PER_MINUTE
    gain_hours_p_year: float = DAYS_PER_YEAR * gain_hours_p_day

    return loaded_wage * gain_hours_p_year


def calculate_annual_gain_wellness_checks(
        loaded_wage: float,  # hourly wage
        gain_wellness_checks_minutes: float,
) -> float:
    gain_hours_p_day: float = gain_wellness_checks_minutes * HOURS_PER_MINUTE
    gain_hours_p_year: float = DAYS_PER_YEAR * gain_hours_p_day

    return loaded_wage * gain_hours_p_year


def calculate_annual_gain_documentation(
        loaded_wage: float,  # hourly wage
        gain_documentation_minutes: float,
) -> float:
    gain_hours_p_day: float = gain_documentation_minutes * HOURS_PER_MINUTE
    gain_hours_p_year: float = DAYS_PER_YEAR * gain_hours_p_day

    return loaded_wage * gain_hours_p_year


def calculate_annual_gain_response_prioritization(
        loaded_wage: float,  # hourly wage
        gain_prioritization_minutes: float,
) -> float:
    gain_hours_p_day: float = gain_prioritization_minutes * HOURS_PER_MINUTE
    gain_hours_p_year: float = DAYS_PER_YEAR * gain_hours_p_day

    return loaded_wage * gain_hours_p_year


def calculate_annual_gain_room_entries(
        loaded_wage: float,  # hourly wage
        gain_room_entries_minutes: float,
) -> float:
    gain_hours_p_day: float = gain_room_entries_minutes * HOURS_PER_MINUTE
    gain_hours_p_year: float = DAYS_PER_YEAR * gain_hours_p_day

    return loaded_wage * gain_hours_p_year


def calculate_annual_gain_delayed_hiring(
        loaded_wage: float,  # hourly wage
        months_delay: float,
        count_positions_delayed: int
) -> float:
    # --- DELAYED HIRING

    hours_delayed: float = (
            count_positions_delayed * months_delay * HOURS_PER_MONTH_1_FTE
    )

    return loaded_wage * hours_delayed
