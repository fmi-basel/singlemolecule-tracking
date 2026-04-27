import os
import argparse
from pathlib import Path

import questionary
import yaml


def build_config(outdir: Path):
    print("CWD:", os.getcwd())
    print("OUTDIR:", outdir)

    # Ask user inputs
    spots_file = questionary.path("Path to spots files:").ask()
    output_dir = questionary.path("Path to output directory:").ask()

    link_distance = float(
        questionary.text(
            "link_distance:",
            validate=lambda v: v.replace(".", "", 1).isdigit()
        ).ask()
    )

    gaps = int(
        questionary.text(
            "gaps:",
            validate=lambda v: v.isdigit()
        ).ask()
    )

    track_length = int(
        questionary.text(
            "track_length:",
            validate=lambda v: v.isdigit()
        ).ask()
    )

    # Use absolute paths (no ambiguity later)
    spots_file = str(Path(spots_file).resolve())
    output_dir = str(Path(output_dir).resolve())

    # Create output directory (fail if exists)
    Path(output_dir).mkdir(parents=True, exist_ok=False)

    config = {
        "spots_file": spots_file,
        "output_dir": output_dir,
        "link_distance": link_distance,
        "gaps": gaps,
        "track_length": track_length,
    }

    # ✅ Write config into WD (not repo root)
    config_path = outdir / "tracking_config.yaml"
    with config_path.open("w") as f:
        yaml.safe_dump(config, f)

    print(f"Config written to: {config_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default=os.environ.get("WD", "."))
    args = parser.parse_args()

    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    build_config(outdir)