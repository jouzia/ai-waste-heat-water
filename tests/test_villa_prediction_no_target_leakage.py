from __future__ import annotations

from types import SimpleNamespace

import scripts.validate_gdr_3m as validation


def _row() -> dict[str, str]:
    return {
        "condition_id": "30-50",
        "feed_inlet_mean_c": "50.0",
        "distillate_inlet_mean_c": "30.0",
        "feed_outlet_mean_c": "37.0",
        "distillate_outlet_mean_c": "42.0",
        "derived_flux_l_m2_h": "4.2",
    }


def test_config_uses_inlet_temperatures_not_observed_outlets(monkeypatch):
    property_temperatures: list[float] = []
    config_kwargs: dict[str, object] = {}

    def fake_water_properties(temp_c: float) -> dict[str, float]:
        property_temperatures.append(temp_c)
        return {"rho": 997.0, "mu": 0.001, "k": 0.6, "cp": 4180.0}

    def fake_htc(temp_c: float, **kwargs: object) -> tuple[float, float, float]:
        return (100.0, 500.0, 7.0)

    def fake_config(**kwargs: object) -> dict[str, object]:
        config_kwargs.update(kwargs)
        return kwargs

    monkeypatch.setattr(validation, "_water_properties", fake_water_properties)
    monkeypatch.setattr(validation, "_htc", fake_htc)
    monkeypatch.setattr(validation, "ChannelConfig", fake_config)

    validation._make_config(
        _row(),
        1.0,
        correlation="watertap",
        geometry="smooth_channel",
        cells=4,
    )

    assert property_temperatures == [50.0, 30.0]
    assert config_kwargs["feed_cp_kj_kg_k"] == 4.18
    assert config_kwargs["permeate_cp_kj_kg_k"] == 4.18


def test_flux_conversion_uses_predicted_not_observed_permeate_outlet(monkeypatch):
    density_temperatures: list[float] = []
    config = SimpleNamespace(membrane_area_m2=2.0, duration_h=1.0)
    predicted_outlet_c = 28.0

    monkeypatch.setattr(
        validation,
        "_make_config",
        lambda *args, **kwargs: (config, {}),
    )
    monkeypatch.setattr(
        validation,
        "simulate_dcmd_channel",
        lambda **kwargs: SimpleNamespace(
            freshwater_produced_kg=2.0,
            feed_out_temperature_c=35.0,
            permeate_out_temperature_c=predicted_outlet_c,
        ),
    )

    def fake_water_properties(temp_c: float) -> dict[str, float]:
        density_temperatures.append(temp_c)
        return {"rho": 1000.0}

    monkeypatch.setattr(validation, "_water_properties", fake_water_properties)

    validation._predict(
        _row(),
        1.0,
        correlation="watertap",
        geometry="smooth_channel",
        cells=4,
    )

    assert density_temperatures == [24.0]
    assert 42.0 not in density_temperatures
