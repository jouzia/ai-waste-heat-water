import pytest

from ai_water.monte_carlo import run_monte_carlo
from ai_water.models import (
    AuxiliaryLoads,
    Cooling,
    HeatRecovery,
    MembraneDistillation,
    Scenario,
    WaterFactors,
    Workload,
)
from ai_water.uncertainty import DistributionSpec


def base_scenario():
    return Scenario(
        workload=Workload(it_power_kw=100.0, duration_h=1.0),
        cooling=Cooling(),
        recovery=HeatRecovery(
            recovery_efficiency=0.5,
            heat_exchanger_effectiveness=0.8,
            source_temperature_c=70.0,
            cold_side_temperature_c=25.0,
        ),
        md=MembraneDistillation(
            flux_kg_m2_h=1.0,
            membrane_area_m2=10.0,
            thermal_energy_kwh_th_per_kg=0.1,
        ),
        auxiliary=AuxiliaryLoads(),
        water=WaterFactors(),
    )


def test_monte_carlo_is_reproducible_for_fixed_seed():
    distributions = {
        "recovery.recovery_efficiency": DistributionSpec("uniform", (0.2, 0.8)),
        "water.avoided_freshwater_consumption_l": DistributionSpec(
            "uniform", (0.0, 2.0)
        ),
    }
    first = run_monte_carlo(
        base_scenario(), distributions, sample_size=20, seed=42
    )
    second = run_monte_carlo(
        base_scenario(), distributions, sample_size=20, seed=42
    )
    assert first.records == second.records
    assert first.successful_samples == 20
    assert first.failed_samples == 0


def test_monte_carlo_counts_invalid_draws_instead_of_clipping():
    result = run_monte_carlo(
        base_scenario(),
        {
            "recovery.recovery_efficiency": DistributionSpec(
                "uniform", (-0.5, 0.5)
            )
        },
        sample_size=50,
        seed=7,
    )
    assert result.successful_samples + result.failed_samples == 50
    assert result.failed_samples > 0
    assert all(
        0.0 <= row["recovery.recovery_efficiency"] <= 1.0
        for row in result.records
    )


def test_monte_carlo_rejects_unknown_parameter_path():
    with pytest.raises(ValueError, match="unknown scenario parameter path"):
        run_monte_carlo(
            base_scenario(),
            {"recovery.not_a_parameter": DistributionSpec("uniform", (0.1, 0.2))},
            sample_size=2,
            seed=1,
        )
