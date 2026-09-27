# Data Dictionary

| Field | Unit | Meaning | Status |
|---|---:|---|---|
| it_power_kw | kW | IT electrical load | scenario/input |
| duration_h | h | modeled operating duration | scenario/input |
| recoverable_heat_fraction | 0–1 | fraction of IT heat considered recoverable before downstream losses | scenario/input |
| facility_overhead_fraction | 0–1+ | facility energy overhead relative to IT energy | scenario/input |
| recovery_efficiency | 0–1 | heat-recovery efficiency | scenario/input |
| heat_exchanger_effectiveness | 0–1 | exchanger effectiveness | scenario/input |
| source_temperature_c | °C | recovered-heat source bulk temperature | scenario/input |
| cold_side_temperature_c | °C | cold-side bulk temperature | scenario/input |
| membrane_permeance_kg_m2_h_bar | kg m^-2 h^-1 bar^-1 | flux coefficient in reduced-order vapor-pressure model | literature/input |
| flux_kg_m2_h | kg m^-2 h^-1 | direct flux for legacy/reproduction cases | literature/input |
| feed_salinity_g_kg | g kg^-1 | inlet feed salinity | scenario/literature input |\n| water_activity | 0–1 | explicit feed-water activity override | literature/property model |
| temperature_polarization_coefficient | 0–1 | reduced-order interface-temperature parameter | literature/model input |
| latent_heat_kwh_th_per_kg | kWh_th kg^-1 | latent vaporization duty | property/input |
| membrane_thermal_conductivity_w_m_k | W m^-1 K^-1 | membrane thermal conductivity | membrane-specific input |
| membrane_thickness_m | m | membrane thickness | membrane-specific input |
| pressure_drop_bar | bar | MD hydraulic pressure loss | literature/measurement |
| pump_efficiency | 0–1 | pump electrical-to-hydraulic efficiency | equipment input |
| feed_recovery_fraction | 0–1 | single-pass distillate/feed ratio | case-specific |\n| concentrate_salinity_g_kg | g kg^-1 | ideal concentrate salinity assuming complete salt retention | model output |
| md_cooling_to_heating_ratio | ratio | thermal cooling duty relative to MD heating duty | configuration-specific |
| md_cooling_electricity_kwh_per_kwh_th | kWh/kWh_th | electricity required per unit cooling duty | heat-sink-specific |
| md_cooling_water_l_per_kwh_th | L/kWh_th | direct cooling-water consumption per unit MD cooling duty | heat-sink-specific |
| grid_water_l_per_kwh | L/kWh | electricity-related water factor under declared boundary | site/grid-specific |
| freshwater_produced_l | L | modeled distillate production | model output |
| feed_water_withdrawal_l | L | feed volume required by recovery fraction | model output |
| concentrate_discharge_l | L | feed minus product, before any recycle | model output |
| additional_water_consumption_l | L | modeled direct + electricity-related operational consumption | model output |
| net_consumption_change_l | L | modeled additional consumption minus recovered freshwater; primary screening sign metric | model output |\n| net_freshwater_benefit_l | L | legacy inverse of net_consumption_change_l; compatibility field only | legacy model output |

Sign convention: Delta_W_net = W_additional_consumption - W_recovered. Negative means recovered freshwater exceeds the modeled additional operational burden; positive means the reverse. This is a screening metric and does not establish avoided consumption without an explicit counterfactual.
