import pytest

from ai_water.workload_profile import (
    WorkloadInterval,
    WorkloadProfileFactors,
    integrate_workload_profile,
)


def test_profile_integrates_time_varying_it_energy_and_heat():
    intervals = [
        WorkloadInterval(
            duration_h=1.0,
            it_power_kw=100.0,
            recoverable_heat_fraction=0.8,
            source_temperature_c=60.0,
        ),
        WorkloadInterval(
            duration_h=0.5,
            it_power_kw=40.0,
            recoverable_heat_fraction=0.5,
            source_temperature_c=70.0,
        ),
    ]
    result = integrate_workload_profile(
        intervals,
        WorkloadProfileFactors(
            recovery_efficiency=0.5,
            heat_exchanger_effectiveness=0.8,
            usable_heat_fraction=1.0,
        ),
    )
    assert result.duration_h == pytest.approx(1.5)
    assert result.it_energy_kwh == pytest.approx(120.0)
    assert result.heat_generated_kwh_th == pytest.approx(120.0)
    assert result.usable_recoverable_heat_kwh_th == pytest.approx(36.0)
    assert result.heat_availability_fraction == pytest.approx(1.0)
    assert result.heat_weighted_source_temperature_c == pytest.approx(
        (60.0 * 32.0 + 70.0 * 4.0) / 36.0
    )


def test_profile_excludes_below_threshold_heat_from_usable_recovery():
    intervals = [
        WorkloadInterval(
            duration_h=1.0,
            it_power_kw=100.0,
            recoverable_heat_fraction=0.8,
            source_temperature_c=35.0,
        ),
        WorkloadInterval(
            duration_h=1.0,
            it_power_kw=100.0,
            recoverable_heat_fraction=0.8,
            source_temperature_c=70.0,
        ),
    ]
    result = integrate_workload_profile(
        intervals,
        WorkloadProfileFactors(
            recovery_efficiency=0.5,
            heat_exchanger_effectiveness=0.8,
            minimum_source_temperature_c=50.0,
        ),
    )
    assert result.it_energy_kwh == pytest.approx(200.0)
    assert result.raw_recoverable_heat_kwh_th == pytest.approx(64.0)
    assert result.usable_recoverable_heat_kwh_th == pytest.approx(32.0)
    assert result.thermally_eligible_duration_h == pytest.approx(1.0)
    assert result.heat_availability_fraction == pytest.approx(0.5)


def test_profile_rejects_empty_trace():
    with pytest.raises(ValueError, match="at least one"):
        integrate_workload_profile([], WorkloadProfileFactors(recovery_efficiency=0.5, heat_exchanger_effectiveness=0.8, usable_heat_fraction=1.0))



def test_profile_does_not_count_idle_intervals_as_heat_available():
    intervals = [
        WorkloadInterval(
            duration_h=1.0,
            it_power_kw=100.0,
            recoverable_heat_fraction=0.8,
            source_temperature_c=65.0,
        ),
        WorkloadInterval(
            duration_h=1.0,
            it_power_kw=0.0,
            recoverable_heat_fraction=0.8,
            source_temperature_c=65.0,
        ),
    ]
    result = integrate_workload_profile(
        intervals,
        WorkloadProfileFactors(recovery_efficiency=0.5, heat_exchanger_effectiveness=0.8, usable_heat_fraction=1.0, minimum_source_temperature_c=50.0),
    )
    assert result.duration_h == pytest.approx(2.0)
    assert result.thermally_eligible_duration_h == pytest.approx(1.0)
    assert result.heat_availability_fraction == pytest.approx(0.5)
