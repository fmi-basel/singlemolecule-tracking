import os
import argparse
import questionary
import yaml
from pathlib import Path


def build_config(outdir: Path):
    cwd = os.getcwd()

    img_file = questionary.path("Path raw/denoised image files:").ask()
    mask_file = questionary.path("Path to cell mask files:").ask()
    actin_file = questionary.path("Path to actin image files:").ask()
    tubulin_file = questionary.path("Path to tubulin image files:").ask()
    output_dir = questionary.path("Path to output directory:").ask()
    NA = float(
        questionary.text("NA:", validate=lambda v: v.replace(".", "").isdigit()).ask()
    )
    wavelength = int(
        questionary.text("Wavelength:", validate=lambda v: v.isdigit()).ask()
    )
    spacing = float(
        questionary.text(
            "Spacing in xy [um]:", validate=lambda v: v.replace(".", "").isdigit()
        ).ask()
    )
    k = float(
        questionary.text(
            "Threshold factor (float):", validate=lambda v: v.replace(".", "").isdigit()
        ).ask()
    )

    config = {
        "img_file": os.path.relpath(img_file, cwd),
        "mask_file": os.path.relpath(mask_file, cwd),
        "actin_file": os.path.relpath(actin_file, cwd),
        "tubulin_file": os.path.relpath(tubulin_file, cwd),
        "output_dir": os.path.relpath(output_dir, cwd),
        "NA": NA,
        "wavelength": wavelength,
        "spacing": (spacing, spacing),
        "k": k,
    }

    os.makedirs(output_dir, exist_ok=False)

    config_path = outdir / "spot_detection_config.yaml"
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default=os.environ.get("WD", "."))
    args = parser.parse_args()

    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    build_config(outdir)