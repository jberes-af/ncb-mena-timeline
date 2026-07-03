# /src/application/services/calculate_iot_cost_npv.py

from src.domain.services.operator_calculations import (
    monthly_discount_rate,
    perform_iot_npv_cost_calculation,
)

from src.application.dto.roi_use_case_dtos import (
    OperatorIotCostDTO
)


def calculate_operator_iot_system_npv_cost_from_config(
        annual_discount_rate: float,
        hardware_cost: float,
        monthly_subscription_cost: float,
        contract_term_months: int,
) -> OperatorIotCostDTO:
    monthly_rate = monthly_discount_rate(annual_discount_rate)

    npv_cost = perform_iot_npv_cost_calculation(
        hardware_cost=hardware_cost,
        monthly_payment=monthly_subscription_cost,
        monthly_rate=monthly_rate,
        months=contract_term_months,
    )

    annualized_iot_cost = npv_cost / (contract_term_months / 12)
    monthly_iot_cost = npv_cost / contract_term_months

    return OperatorIotCostDTO(
        npv_cost=npv_cost,
        monthly_iot_cost=monthly_iot_cost,
        annualized_iot_cost=annualized_iot_cost,
    )
