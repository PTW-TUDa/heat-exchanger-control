from __future__ import annotations

import pathlib

from eta_ctrl import EtaCtrl, get_logger

def experiment() -> None:
    """Control of the heat exchanger following a rulebased strategy. """
    get_logger(level=1, log_format="logname")
    root_path = pathlib.Path(__file__).parent
    experiment = EtaCtrl(root_path=root_path, config_name="experiment_config")
    experiment.play(series_name="pwt_control", run_name="vergleichs_run")
    
if __name__ == "__main__":
    experiment()
