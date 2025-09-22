from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

import pyomo.environ as pyo

from eta_ctrl.envs import LiveEnv

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from typing import Any


log = getLogger(__name__)

class Pwt(LiveEnv):
    version = "0.1.0"
    description = "Environment for controlling the power of PWT1 at ETA."
    config_name = "glt_hnht_only"
    
    def __init__(self, scenario_files, **kwargs) -> None:
        super().__init__(**kwargs)
        self.timeseries = self.import_scenario(*scenario_files)  # Load time series data

    def render(self) -> None:
        pass
