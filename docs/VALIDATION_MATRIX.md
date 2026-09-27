# Validation Matrix

| Layer | Validation target | Evidence | Current status |
|---|---|---|---|
| Saturation pressure | Pure-water vapor pressure | NIST SRD 69 | Implemented; CI regression required |
| Seawater activity | Standard-seawater chemical potential/activity | IAPWS R13-08 | Implemented; independent numeric checks required |
| Single-pass concentration | Salt-retention mass balance | Conservation equation | Implemented |
| DCMD axial energy balance | Feed/permeate temperature evolution | Keshavarzzadeh et al. 2020 | Source-matched benchmark registered |
| Heat-transfer correlations | h_f/h_p sensitivity | MD literature + WaterTAP | Implemented as selectable primitives; source-range validation pending |
| Concentration polarization | CPC/interface salinity | MD CP literature | Implemented as selectable reduced-order model; experimental validation pending |
| Cooling burden | Heating/cooling/pumping accounting | Malaguti et al. 2026 | System boundary implemented; source reproduction pending |
| Water accounting | Withdrawal vs consumption vs recovered water | Data-center water literature | Accounting structure implemented |
| Geographic stress | Site/basin water-stress layer | WRI Aqueduct 4.0 | Schema registered; dataset acquisition pending |
| Full coupled result | Sign of Delta_W_net under uncertainty | Multi-source | Not yet claimed |
