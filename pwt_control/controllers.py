from eta_ctrl.agents.rule_based import RuleBased
from numpy import asarray


class PwtController(RuleBased):
    def control_rules(self, observation):
        if observation["pwt_system_state"] != 4 or observation["hnht_algorithm_permission"] == 0:
            action = [-1.0]
        else:
            action = -(
                observation["hex1_thermal_load"]
                + observation["static_heating_thermal_load"]
                + observation["central_machine_heating_thermal_load"]
            )
        return asarray(action)


PREHEATING_ACTION_VALUES = {
    "HNHT_HNLT.HeatExchanger1System.control.bSetStatusOnAlgorithm": True,
    "HNHT_HNLT.HeatExchanger1System.PU215.control.bSetStatusOnAlgorithm": False,
    "HNHT_HNLT.HeatExchanger1System.RV315.control.bSetStatusOnAlgorithm": True,
    "HNHT_HNLT.HeatExchanger1System.RV315.localSetParameters.nControlModeAlgorithm": 0,
    "HNHT_HNLT.HeatExchanger1System.RV315.setSetPoint.fSetPointAlgorithm": 100.0,
    "HNHT.CHP2System.control.bSetStatusOnAlgorithm": False,
    "HNHT.CHP2System.PU32x.control.bSetStatusOnAlgorithm": True,
    "HNHT.CHP2System.PU32x.setSetPoint.fSetPointAlgorithm": 100.0,
    "HNHT.CHP2System.RV32x.control.bSetStatusOnAlgorithm": True,
    "HNHT.CHP2System.RV32x.localSetParameters.nControlModeAlgorithm": 0,
    "HNHT.CHP2System.RV32x.setSetPoint.fSetPointAlgorithm": 100.0,
    "HNHT.CHP2System.SV32x.control.bSetStatusOnAlgorithm": True,
    "HNHT.VSIStorageSystem.control.bSetStatusOnAlgorithm": True,
    "HNHT.VSIStorageSystem.localSetParameters.bLoadingAlgorithm": True,
    "HNHT.VSIStorageSystem.SV307.control.bSetStatusOnAlgorithm": True,
    "HNHT.VSIStorageSystem.SV307.setSetPoint.fSetPointAlgorithm": 100.0,
}


class PrepareHnht(RuleBased):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions_order = self.get_env().get_attr("state_config", 0)[0].actions

    def control_rules(self, observation):
        missing_actions = [name for name in self.actions_order if name not in PREHEATING_ACTION_VALUES]
        if missing_actions:
            msg = f"Missing action values for: {', '.join(missing_actions)}"
            raise KeyError(msg)

        action = [PREHEATING_ACTION_VALUES[name] for name in self.actions_order]
        return asarray(action, dtype=float)
