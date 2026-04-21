from eta_ctrl.agents.rule_based import RuleBased
import numpy as np
from logging import getLogger


log = getLogger(__name__)


class HysteresisController:
    """
    A simple hysteresis (on/off) controller using explicit thresholds.

    The controller switches its output based on an input value relative to a
    lower and upper threshold. This prevents rapid toggling ("chattering")
    when the input is between the thresholds.

    Parameters
    ----------
    lower_threshold : float
        Lower switching threshold.
    upper_threshold : float
        Upper switching threshold.
    inverted : bool, optional
        If False (default):
            - Output turns ON when value <= lower_threshold
            - Output turns OFF when value >= upper_threshold
            (typical for heating)

        If True:
            - Output turns ON when value >= upper_threshold
            - Output turns OFF when value <= lower_threshold
            (typical for cooling)

    init_value : bool, optional
        Initial output state (False = OFF, True = ON)

    Notes
    -----
    The region between lower_threshold and upper_threshold is the "deadband"
    where the output does not change state.
    """

    def __init__(self, lower_threshold, upper_threshold, inverted=False, init_value=False):
        if lower_threshold > upper_threshold:
            raise ValueError("lower_threshold must be <= upper_threshold")

        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.inverted = inverted
        self.output = bool(init_value)

    def get_action(self, actual_value):
        actual_value = np.asarray(actual_value).item()  # force scalar

        if not self.output:
            if self.inverted:
                self.output = actual_value >= self.upper_threshold
            else:
                self.output = actual_value <= self.lower_threshold
        else:
            if self.inverted:
                self.output = actual_value > self.lower_threshold
            else:
                self.output = actual_value < self.upper_threshold

        return bool(self.output)


class PwtController(RuleBased):
    """
    This controller sets the HEX1 set point and activates/deactivates the production mode.

    In addition, the controller uses three-stage recooling with hysteresis based on the mid buffer temperature.

    Each system switches on/off at defined thresholds to avoid rapid toggling.

    Activation thresholds
    Consumers: ON ≥ 30 °C, OFF ≤ 28 °C
    AFA: ON ≥ 34 °C, OFF ≤ 29 °C (starts ON) (set point is fixed at 32 °C)
    HVFA: ON ≥ 36 °C, OFF ≤ 32 °C
    Temperature sequence
    Rising temperature:
    Consumers → AFA → HVFA
    Decreasing temperature:
    HVFA → AFA → Consumers
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions_order = self.get_env().get_attr("state_config", 0)[0].actions

        self.controller_facade = HysteresisController(
            lower_threshold=29, upper_threshold=34, inverted=True, init_value=True
        )
        self.controller_hvfa = HysteresisController(lower_threshold=32, upper_threshold=36, inverted=True)
        self.controller_hnlt_consumers = HysteresisController(lower_threshold=28, upper_threshold=30, inverted=True)

    def control_rules(self, observation):
        action = dict.fromkeys(self.actions_order, None)  # get a dict with all action names set to None

        if observation["pwt_system_state"] != 4:
            action["HNHT_HNLT.HeatExchanger1System.RV315.setSetPoint.fSetPointAlgorithm"] = 0
        else:
            hex1_load = np.asarray(observation["hex1_thermal_load"]).item()
            static_heating_load = np.asarray(observation["static_heating_thermal_load"]).item()
            central_machine_load = np.asarray(observation["central_machine_heating_thermal_load"]).item()

            action["HNHT_HNLT.HeatExchanger1System.RV315.setSetPoint.fSetPointAlgorithm"] = -(
                hex1_load + static_heating_load + central_machine_load
            )
        # action productionmode
        action["Strategy.localSetParameters.bProductionModeActivated"] = bool(
            np.asarray(observation["bproductionmodeactivated"]).item()
        )

        # control recooling
        mid_buffer_temp = observation["HNLT.localState.fMidTemperature"]

        action["HNLT.OuterCapillaryTubeMats.control.bSetStatusOnAlgorithm"] = self.controller_facade.get_action(
            mid_buffer_temp
        )
        action["HNLT.HVFASystem.control.bSetStatusOnAlgorithm"] = self.controller_hvfa.get_action(mid_buffer_temp)

        action_consumer = self.controller_hnlt_consumers.get_action(
            mid_buffer_temp
        )  # true, if consumer can consumer energy
        # invert signal to deactivate algorithm mode
        action["HNLT_CN.InnerCapillaryTubeMats.control.bAlgorithmModeActivated"] = not action_consumer
        action["HNLT_CN.UnderfloorHeatingSystem.control.bAlgorithmModeActivated"] = not action_consumer

        if not observation["hnht_algorithm_permission"]:
            # if HNHT has no algorithm permission, recooling of HNLT should be stopped
            action["HNLT.OuterCapillaryTubeMats.control.bSetStatusOnAlgorithm"] = False
            action["HNLT.HVFASystem.control.bSetStatusOnAlgorithm"] = False
            action["HNLT_CN.InnerCapillaryTubeMats.control.bAlgorithmModeActivated"] = False
            action["HNLT_CN.UnderfloorHeatingSystem.control.bAlgorithmModeActivated"] = False

        log.info(action)

        return self._aggregate_actions(action)

    def _aggregate_actions(self, action: dict) -> np.ndarray:
        """Aggregate actions from multiple environments.

        :param actions: dictionary of actions.
        :returns: Aggregated actions as np array, which is accepted by eta-ctrl rule based controller.
        """
        # check that all actions have been set
        for key, value in action.items():
            if value is None:
                raise ValueError(f"Action '{key}' has not been set in the control_rules function.")
        actions = list(action.values())

        return np.array(actions)
