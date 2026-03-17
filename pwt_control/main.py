from __future__ import annotations

import pathlib

from eta_ctrl import EtaCtrl, get_logger


def preparation() -> None:
    """Rule-based control of the heat exchanger.
    CAUTION: This is a live experiment, starting this file will connect to the physical heat exchanger!"""
    get_logger(level=1, log_format="logname")
    root_path = pathlib.Path(__file__).parent
    experiment = EtaCtrl(root_path=root_path, config_relpath="", config_name="preparation")
    experiment.play(series_name="preparation_hnht", run_name="20260313_preparation_hnht")


def experiment() -> None:
    """Rule-based control of the heat exchanger.
    CAUTION: This is a live experiment, starting this file will connect to the physical heat exchanger!"""
    get_logger(level=1, log_format="logname")
    root_path = pathlib.Path(__file__).parent
    experiment = EtaCtrl(root_path=root_path, config_relpath="", config_name="aae_experiment")
    experiment.play(series_name="experiment_aae_3d", run_name="live_run_test")


if __name__ == "__main__":
    # preparation()
    experiment()
