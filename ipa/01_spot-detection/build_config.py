import os
import questionary
import yaml

def build_config():
    cwd = os.getcwd()

    img_file = questionary.path("Path raw/denoised image file:").ask()
    mask_file = questionary.path("Path to cell mask file:").ask()
    output_dir = questionary.path("Path to output directory:").ask()


    config = {
        "img_file": os.path.relpath(img_file, cwd),
        "mask_file": os.path.relpath(mask_file, cwd),
        "output_dir": os.path.relpath(output_dir, cwd),
    }

    os.makedirs(output_dir, exist_ok=False)

    with open(os.path.join(cwd, "spot_detection_config.yaml"), "w") as f:
        yaml.safe_dump(config, f)


if __name__ == "__main__":
    build_config()
