from ai_water.demo import run_demo


def test_demo_preserves_gross_water_and_net_accounting_separately():
    output = run_demo()
    water = output["water"]

    assert output["status"] == "illustrative_demo_only"
    assert output["scientific_claim"] is False
    assert water["gross_distillate_l"] > 0
    assert water["declared_avoided_freshwater_consumption_l"] == 0
    assert water["net_consumption_change_l"] == water["additional_water_consumption_l"]
    assert water["interpretation"] == "neutral_vs_counterfactual"


def test_demo_reports_heat_quality():
    output = run_demo()
    energy = output["energy_and_heat"]

    assert energy["source_heat_exergy_kwh"] > 0
    assert energy["recoverable_heat_exergy_kwh"] > 0
    assert energy["recoverable_heat_exergy_kwh"] < energy["source_heat_exergy_kwh"]
