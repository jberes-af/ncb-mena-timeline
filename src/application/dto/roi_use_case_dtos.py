# /src/application/dto/roi_use_case_dtos.py

from dataclasses import dataclass

from src.domain.entities.entities import (
    FacilityProfile,
    IotSystemConfiguration,
    EfficiencyAssumptions
)


@dataclass(frozen=True)
class CalculationInputsDTO:
    facility: FacilityProfile
    iot_system_config: IotSystemConfiguration
    assumptions: EfficiencyAssumptions


@dataclass(frozen=True)
class OperatorBenefitsDTO:
    efficiency_annual_overnight_rounds: float
    efficiency_annual_wellness_checks: float
    efficiency_annual_documents: float
    efficiency_annual_prioritization: float
    efficiency_annual_room_entries: float
    efficiency_annual_total: float
    delayed_hiring_value_annual: float

    staff_payroll_annual: float
    percent_efficiency: float

    added_residents_theoretical: float
    added_residents_use_case: float
    contribution_margin_annualized: float
    new_resident_value_monthly: float
    new_resident_value_annual: float


@dataclass(frozen=True)
class OperatorIotCostDTO:
    npv_cost: float
    monthly_iot_cost: float
    annualized_iot_cost: float


@dataclass(frozen=True)
class CalculateRoiResultDTO:
    hardware_cost: float
    monthly_subscription_cost: float
    contract_term_months: int

    npv_iot_cost: float
    monthly_iot_cost: float
    annualized_iot_cost: float

    efficiency_overnight_rounds: float
    efficiency_wellness_checks: float
    efficiency_documents: float
    efficiency_prioritization: float
    efficiency_room_entries: float
    efficiency_total: float

    delayed_hiring_value: float

    staff_payroll_annual: float
    iot_percent_efficiency: float

    contribution_margin: float
    added_residents_theoretical: float
    added_residents_use_case: float
    new_resident_value_theoretical: float
    new_resident_value_use_case: float

    net_annual_benefit: float
    roi_percent: float
    payback_months: float | None
