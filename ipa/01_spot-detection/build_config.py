import os
import questionary
import yaml

def build_config():
    cwd = os.getcwd()

    img_file = questionary.path("Path raw/denoised image files:").ask()
    mask_file = questionary.path("Path to cell mask files:").ask()
    output_dir = questionary.path("Path to output directory:").ask()
    NA = float(questionary.text(
        "NA:", 
        validate=lambda v: v.replace(".", "").isdigit()
    ).ask())
    wavelength = int(questionary.text(
        "wavelength:",
        validate=lambda v: v.isdigit()
    ).ask())
    spacing = float(questionary.text(
        "Spacing in xy [um]:",
        validate=lambda v: v.replace(".", "").isdigit()
    ).ask())
    k = float(questionary.text(
        "Threshold factor (float):",
        validate=lambda v: v.replace(".", "").isdigit()
    ).ask())

    config = {
        "img_file": os.path.relpath(img_file, cwd),
        "mask_file": os.path.relpath(mask_file, cwd),
        "output_dir": os.path.relpath(output_dir, cwd),
        "NA": NA,
        "wavelength": wavelength,
        "spacing": (spacing, spacing),
        "k": k
    }

    os.makedirs(output_dir, exist_ok=False)

    with open(os.path.join(cwd, "spot_detection_config.yaml"), "w") as f:
        yaml.safe_dump(config, f)


if __name__ == "__main__":
    build_config()
