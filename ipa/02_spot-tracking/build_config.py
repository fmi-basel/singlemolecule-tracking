import os
import questionary
import yaml

def build_config():
    cwd = os.getcwd()

    spots_file = questionary.path("Path spots files:").ask()
    output_dir = questionary.path("Path to output directory:").ask()
    linkdis = float(questionary.text(
        "linkdis:", 
        validate=lambda v: v.replace(".", "").isdigit()
    ).ask())
    gaps = int(questionary.text(
        "gaps:",
        validate=lambda v: v.isdigit()
    ).ask())
    tracklen = int(questionary.text(
        "tracklen:",
        validate=lambda v: v.isdigit()
    ).ask())
    
    config = {
        "spots_file": os.path.relpath(spots_file, cwd),
        "output_dir": os.path.relpath(output_dir, cwd),
        "linkdis": linkdis,
        "gaps": gaps,
        "tracklen": tracklen
    }

    os.makedirs(output_dir, exist_ok=False)

    with open(os.path.join(cwd, "tracking_config.yaml"), "w") as f:
        yaml.safe_dump(config, f)


if __name__ == "__main__":
    build_config()