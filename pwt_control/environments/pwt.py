from __future__ import annotations

from logging import getLogger


from eta_ctrl.envs import LiveEnv


log = getLogger(__name__)


class Pwt(LiveEnv):
    @property
    def version(_):
        return "0.1.0"

    @property
    def description(_):
        return "Environment for controlling the power of PWT1 at ETA."

    @property
    def config_name(_):
        return "glt_hnht_only"

    def render(self) -> None:
        pass
