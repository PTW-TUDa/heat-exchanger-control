from __future__ import annotations

from logging import getLogger
from pathlib import Path


from eta_ctrl.envs import LiveEnv
import numpy as np
import pandas as pd


log = getLogger(__name__)


class Hnht(LiveEnv):
    @property
    def version(_):
        return "0.1.0"

    @property
    def description(_):
        return "Environment for homogenization of temperatures in HNHT."

    @property
    def config_name(_):
        return "prepare_hnht"

    def render(self) -> None:
        # create episode dataframe
        self.episode_df = pd.DataFrame(self.state_log)

        # Flatten numpy arrays to scalars so that pandas methods work correctly
        self.episode_df = self.episode_df.map(lambda v: v.item() if isinstance(v, np.ndarray) and v.size == 1 else v)

        # Apply standard cleanup (now working on floats/scalars)
        self.episode_df = self.episode_df.bfill().infer_objects(copy=False)

        file_name_prefix = f"{self.config_run.name}_{self.n_episodes:03d}-{self.env_id:02d}"

        # define file names
        self.file_name_episode_df_raw = Path(f"{file_name_prefix}_episode_raw.csv")

        # save raw df without any cleaning
        self.episode_df.to_csv(
            path_or_buf=Path(self.series_results_path) / self.file_name_episode_df_raw,
            sep=";",
            decimal=",",
        )
