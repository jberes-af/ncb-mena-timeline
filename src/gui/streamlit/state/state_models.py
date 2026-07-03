# /src/gui/streamlit/state/state_models.py

from dataclasses import dataclass


@dataclass
class RoiInputState:
    resident_count: int = 10
    caregiver_count: int = 6
    # annual_caregiver_payroll: float = 274000.0
    monthly_revenue_per_resident: float = 5500.0
    monthly_variable_cost_per_resident: float = 3000.0

    kit_installations: int = 10
    hardware_cost: float = 0.0
    # monthly_cost: float = 1030.0
    contract_months: int = 24
    annual_discount_rate: float = 0.10

    caregiver_efficiency_gain: float = 0.10
    occupancy_lift_residents: float = 1.0
    overnight_hours_saved_per_night: float = 0.5
    loaded_hourly_wage: float = 22.0

    gain_overnight_rounds: int = 40
    gain_wellness_checks: int = 60
    gain_documentation: int = 45
    gain_response_prioritization: int = 45
    gain_room_entries: int = 90

    gain_hiring_delay: int = 1
    count_positioned_delayed: int = 1


