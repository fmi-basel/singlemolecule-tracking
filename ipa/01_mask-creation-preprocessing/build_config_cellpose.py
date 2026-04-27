import os
import questionary
import yaml
import re


def build_config():
    cwd = os.getcwd()

    input_path = questionary.path("Input path max projections:").ask()
    whole_cell_model = questionary.path("Path to model:").ask()

    n_iter = int(
        questionary.text(
            "Number of iterations:",
            default="2000",
            validate=lambda v: v.isdigit()
        ).ask()
    )

    cellprob_threshold = float(
        questionary.text(
            "Cell probability threshold (float):",
            default="0.0",
            validate=lambda v: re.fullmatch(r"-?\d+(\.\d+)?", v) is not None
        ).ask()
    )

    flow_threshold = float(
        questionary.text(
            "Flow threshold (float):",
            default="0.9",
            validate=lambda v: v.replace(".", "", 1).isdigit() and v.count(".") <= 1
        ).ask()
    )

    config = {
        "input_path": os.path.relpath(input_path, cwd),
        "whole_cell_model": os.path.relpath(whole_cell_model, cwd),
        "n_iter": n_iter,
        "cellprob_threshold": cellprob_threshold,
        "flow_threshold": flow_threshold,
    }

    with open(os.path.join(cwd, "cellpose_config.yaml"), "w") as f:
        yaml.safe_dump(config, f)


if __name__ == "__main__":
    build_config()