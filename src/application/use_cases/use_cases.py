# /src/application/use_cases/use_cases.py

from src.domain.services.operator_calculations import annuity_present_value

from src.domain.entities.entities import (
    FacilityProfile,
    IotSystemConfiguration,
    EfficiencyAssumptions,
)

from src.application.dto.roi_use_case_dtos import (
    OperatorBenefitsDTO,
    OperatorIotCostDTO,
    CalculateRoiResultDTO,
)

from src.application.services.calculate_operator_benefits import (
    OperatorBenefitsCalculator,
)

from src.application.services.calculate_operator_efficiencies import (
    calculate_annual_gain_overnight_rounds,
    calculate_annual_gain_wellness_checks,
    calculate_annual_gain_documentation,
    calculate_annual_gain_response_prioritization,
    calculate_annual_gain_room_entries,
    calculate_annual_gain_delayed_hiring,
)

from src.application.services.calculate_iot_cost_npv import (
    calculate_operator_iot_system_npv_cost_from_config,
)


class CalculateRoiUseCase:
    def __init__(
            self,
            calculate_benefits: OperatorBenefitsCalculator,
    ) -> None:
        self._calculate_benefits = calculate_benefits

    def execute(
            self,
            facility: FacilityProfile,
            iot_system_config: IotSystemConfiguration,
            assumptions: EfficiencyAssumptions,
    ) -> CalculateRoiResultDTO:
        operator_benefits: OperatorBenefitsDTO = self._calculate_operator_benefits(
            facility=facility,
            assumptions=assumptions,
        )

        kit_count: int = iot_system_config.kit_installations

        hardware_cost: float = (
                kit_count * iot_system_config.selected_kit_price
        )

        monthly_subscription_cost: float = (
                kit_count * iot_system_config.monthly_subscription_price
        )

        iot_cost: OperatorIotCostDTO = calculate_operator_iot_system_npv_cost_from_config(
            annual_discount_rate=iot_system_config.annual_discount_rate,
            hardware_cost=hardware_cost,
            monthly_subscription_cost=monthly_subscription_cost,
            contract_term_months=iot_system_config.contract_months,
        )

        operator_benefit_npv: float = annuity_present_value(
            monthly_amount=operator_benefits.new_resident_value_monthly,
            months=iot_system_config.contract_months,
            annual_rate=iot_system_config.annual_discount_rate,
        )

        annualized_operator_benefit_npv = (
                operator_benefit_npv / (iot_system_config.contract_months / 12)
        )

        gross_monthly_benefit = (
                operator_benefit_npv / iot_system_config.contract_months
        )

        net_npv = operator_benefit_npv - iot_cost.npv_cost

        annualized_net_npv = (
                net_npv / (iot_system_config.contract_months / 12)
        )

        monthly_equivalent_net_npv = (
                net_npv / iot_system_config.contract_months
        )

        gross_payback_months = (
            iot_cost.npv_cost / gross_monthly_benefit
            if gross_monthly_benefit > 0
            else None
        )

        net_roi = (
            net_npv / iot_cost.npv_cost
            if iot_cost.npv_cost > 0
            else 0
        )

        """
        _print_to_shell_iot_costs(
            iot_system_config,
            iot_cost_annual,
            operator_added_resident_npv,
            annualized_operator_added_resident_npv,
            net_npv,
            annualized_net_npv,
            monthly_net_npv,
            net_benefit_annualized,
            payback,
        )
        """


        return CalculateRoiResultDTO(
            hardware_cost=hardware_cost,
            monthly_subscription_cost=monthly_subscription_cost,
            contract_term_months=iot_system_config.contract_months,

            npv_iot_cost=iot_cost.npv_cost,
            monthly_iot_cost=iot_cost.monthly_iot_cost,
            annualized_iot_cost=iot_cost.annualized_iot_cost,

            efficiency_overnight_rounds=operator_benefits.efficiency_annual_overnight_rounds,
            efficiency_wellness_checks=operator_benefits.efficiency_annual_wellness_checks,
            efficiency_documents=operator_benefits.efficiency_annual_documents,
            efficiency_prioritization=operator_benefits.efficiency_annual_prioritization,
            efficiency_room_entries=operator_benefits.efficiency_annual_room_entries,
            efficiency_total=operator_benefits.efficiency_annual_total,
            delayed_hiring_value=operator_benefits.delayed_hiring_value_annual,

            staff_payroll_annual=operator_benefits.staff_payroll_annual,
            iot_percent_efficiency=operator_benefits.percent_efficiency,

            contribution_margin=operator_benefits.contribution_margin_annualized,
            added_residents_theoretical=operator_benefits.added_residents_theoretical,
            added_residents_use_case=operator_benefits.added_residents_use_case,

            new_resident_value_theoretical=operator_benefits.new_resident_value_annual,
            new_resident_value_use_case=operator_benefits.new_resident_value_monthly,

            net_annual_benefit=annualized_net_npv,
            roi_percent=net_roi,
            payback_months=gross_payback_months,
        )

    def _calculate_operator_benefits(
            self,
            facility: FacilityProfile,
            assumptions: EfficiencyAssumptions,
    ) -> OperatorBenefitsDTO:
        loaded_wage = facility.loaded_hourly_wage

        overnight_rounds = calculate_annual_gain_overnight_rounds(
            loaded_wage=loaded_wage,
            gain_overnight_rounds_minutes=assumptions.gain_overnight_rounds,
        )

        wellness_checks = calculate_annual_gain_wellness_checks(
            loaded_wage=loaded_wage,
            gain_wellness_checks_minutes=assumptions.gain_wellness_checks,
        )

        documents = calculate_annual_gain_documentation(
            loaded_wage=loaded_wage,
            gain_documentation_minutes=assumptions.gain_documentation,
        )

        prioritization = calculate_annual_gain_response_prioritization(
            loaded_wage=loaded_wage,
            gain_prioritization_minutes=assumptions.gain_response_prioritization,
        )

        room_entries = calculate_annual_gain_room_entries(
            loaded_wage=loaded_wage,
            gain_room_entries_minutes=assumptions.gain_room_entries,
        )

        hiring_delay = calculate_annual_gain_delayed_hiring(
            loaded_wage=loaded_wage,
            months_delay=assumptions.hiring_delay_months,
            count_positions_delayed=assumptions.count_positions_delayed,
        )

        total_efficiencies_annual = (
                overnight_rounds
                + wellness_checks
                + documents
                + prioritization
                + room_entries
                + hiring_delay
        )

        (
            staff_payroll_annual,
            percent_efficiency,
            added_residents_theoretical,
            added_residents_use_case,
        ) = self._calculate_benefits.calculate_unused_capacity(
            resident_count=facility.resident_count,
            caregiver_count=facility.caregiver_count,
            loaded_wage=loaded_wage,
            total_efficiencies_annual=total_efficiencies_annual,
        )

        (
            annualized_margin,
            added_resident_value_monthly,
            added_resident_value_annual,
        ) = self._calculate_benefits.calculate_added_resident_value(
            added_capacity=added_residents_use_case,
            monthly_revenue=facility.monthly_revenue_per_resident,
            monthly_cost=facility.monthly_variable_cost_per_resident,
        )

        return OperatorBenefitsDTO(
            efficiency_annual_overnight_rounds=overnight_rounds,
            efficiency_annual_wellness_checks=wellness_checks,
            efficiency_annual_documents=documents,
            efficiency_annual_prioritization=prioritization,
            efficiency_annual_room_entries=room_entries,
            efficiency_annual_total=total_efficiencies_annual,
            delayed_hiring_value_annual=hiring_delay,

            staff_payroll_annual=staff_payroll_annual,
            percent_efficiency=percent_efficiency,
            added_residents_theoretical=added_residents_theoretical,
            added_residents_use_case=added_residents_use_case,
            contribution_margin_annualized=annualized_margin,
            new_resident_value_monthly=added_resident_value_monthly,
            new_resident_value_annual=added_resident_value_annual,
        )


def _print_to_shell_iot_costs(
        assumptions: IotSystemConfiguration,
        cost_object: OperatorIotCostDTO,
        operator_added_resident_npv: float,
        annualized_operator_added_resident_npv: float,
        net_npv: float,
        annualized_net_npv: float,
        monthly_net_npv: float,
        net_benefit_annualized: float,
        payback: float,
):
    print("Alerta Home Operator DCF Costs:")
    print(f"Annual Discount Rate  : {100 * assumptions.annual_discount_rate:.1f}%")
    print(f"Period (months)       : {assumptions.contract_months}")
    print(f"NPV ($)               : {cost_object.npv_cost:,.2f}")
    print(f"Annualized ($)        : {cost_object.annualized_iot_cost:,.2f}")
    print(f"Monthly ($)           : {cost_object.monthly_iot_cost:,.2f}")
    print()
    print(f"operator_added_resident_npv ($)           : {operator_added_resident_npv:,.2f}")
    print(f"annualized_operator_added_resident_npv ($): {annualized_operator_added_resident_npv:,.2f}")
    print(f"net_npv ($)                               : {net_npv:,.2f}")
    print(f"annualized_net_npv ($)                    : {annualized_net_npv:,.2f}")
    print(f"net_benefit_annualized ($)                : {net_benefit_annualized:,.2f}")
    print(f"monthly_net_npv ($)                       : {monthly_net_npv:,.2f}")
    print(f"payback (months)                          : {payback:,.2f}")
    print()
    print()
