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
