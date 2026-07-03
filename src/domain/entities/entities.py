# /src/domain/entities/entities.py

from dataclasses import dataclass
from enum import Enum


class KitType(str, Enum):
    ONE_PIECE = "ONE_PIECE"
    TWO_PIECE = "TWO_PIECE"
    THREE_PIECE = "THREE_PIECE"
    FOUR_PIECE = "FOUR_PIECE"


@dataclass(frozen=True)
class FacilityProfile:
    resident_count: int
    caregiver_count: int
    # annual_caregiver_payroll: float
    monthly_revenue_per_resident: float
    monthly_variable_cost_per_resident: float
    loaded_hourly_wage: float


"""
@dataclass(frozen=True)
class IotSystemConfiguration:
    kit_type: str
    subscription_price: float
    contract_months: int
    annual_discount_rate: float
"""


@dataclass(frozen=True)
class IotSystemConfiguration:
    selected_kit_type: str
    selected_kit_price: float
    monthly_subscription_price: float
    contract_months: int
    annual_discount_rate: float
    kit_installations: int


@dataclass(frozen=True)
class EfficiencyAssumptions:
    # caregiver_efficiency_gain: float
    # occupancy_lift_residents: float
    # overnight_hours_saved_per_night: float
    # loaded_hourly_wage: float
    gain_overnight_rounds: float
    gain_wellness_checks: float
    gain_documentation: float
    gain_response_prioritization: float
    gain_room_entries: float
    hiring_delay_months: int
    count_positions_delayed: int


@dataclass(frozen=True)
class IotPricingCatalog:
    price_monthly_subscription: float = 89.00
    price_kit_one_piece: float = 225.00
    price_kit__two_piece: float = 255.00
    price_kit_three_piece: float = 312.00
    price_kit_four_piece: float = 320.00
