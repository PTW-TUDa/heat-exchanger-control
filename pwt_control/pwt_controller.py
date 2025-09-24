
from eta_ctrl.agents.rule_based import RuleBased
from numpy import asarray


class PwtController(RuleBased):
    def control_rules(self, observation):
        if observation["pwt_system_state"] != 4:
            action = [0.0]
        else:
            action = observation["lastverlauf"]
        return asarray(action)