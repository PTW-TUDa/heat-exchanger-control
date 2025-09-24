
from eta_ctrl.agents.rule_based import RuleBased
from numpy import asarray


class PwtController(RuleBased):
    def control_rules(self, observation):
        if observation["pwt_system_state"] != 4:
            action = [1,1,1,1,3,0]
        else:
            action = [1,1,1,1,3,observation["HKK_HWV.300.ThHy_P.WMZ300"]]
        return asarray(action)