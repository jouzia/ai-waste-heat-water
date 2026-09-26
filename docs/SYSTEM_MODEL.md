# Coupled System Model

The study evaluates AI/data-center waste heat as a possible thermal input to membrane distillation while accounting for cooling, pumping, electricity-related water, and geographic constraints.

## Coupling chain

AI workload -> IT electricity -> IT heat -> cooling architecture -> recoverable heat -> heat exchanger -> MD interface temperatures -> vapor-pressure driving force -> permeate flux -> freshwater -> cooling/pumping/pretreatment -> water accounting.

## Thermal boundary

As a first-order screening approximation, IT electricity is represented as heat generated at approximately one-to-one energy equivalence. Recoverable heat is:

Q_recoverable = E_IT * f_recoverable * eta_recovery * epsilon_HX * f_usable

This is not a claim that all generated heat is usable. Temperature, duration, exchanger effectiveness, cooling architecture, and heat-sink availability remain explicit constraints.

## Membrane distillation

The current transport primitive uses J = C_m [p_sat(T_fi) - p_sat(T_pi)]. Pure-water saturation pressure is based on NIST SRD 69 Antoine coefficients. The next model stage must use membrane-interface temperatures and water activity for saline feed rather than treating bulk temperatures as the interface state.

The thermal model must distinguish hot-side supply, latent heat, conductive membrane heat leak, sensible heating/cooling, cold-side rejection, heat recovery, and pumping electricity.

## Cooling boundary

Cooling is a first-class variable. Recent system-level MD analysis reports cooling burdens that can approach the magnitude of heating in some configurations and identifies pumping as material at low single-pass recovery. Therefore the model must not infer viability from free heat alone.

## Water accounting

Withdrawal, consumption, and recovered freshwater are separate quantities. The primary operational metric is net consumption change:

Delta W_net = W_additional_consumption - W_recovered

where W_additional_consumption includes direct cooling consumption, auxiliary burdens, and electricity-related water consumption. Negative Delta W_net indicates an offsetting net-consumption effect; zero is break-even; positive is additional consumption.

Withdrawal is reported separately and is never substituted for consumption.

## Uncertainty

The final study should use distributions rather than unsupported point values where evidence permits. Uncertainty classes are parameter, measurement, model-form, scenario, and system-boundary uncertainty. Global sensitivity analysis should identify the parameters controlling the sign and magnitude of Delta W_net.

## Evidence anchors

Lei et al. (2025) show workload-level data-center water use is highly site and workload dependent, with server efficiency, grid water factors, utilization, cooling, infrastructure, climate, and refresh cycle among the key determinants. Malaguti et al. (2026) show that MD cooling and pumping burdens can materially constrain waste-heat pathways. NIST SRD 69 supplies the implemented pure-water saturation-pressure coefficients.

These sources motivate the architecture; they do not validate the complete coupled model.
