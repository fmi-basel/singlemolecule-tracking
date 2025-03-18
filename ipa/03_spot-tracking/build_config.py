import os
import questionary
import yaml

def build_config():
    cwd = os.getcwd()

    spots_file = questionary.path("Path spots files:").ask()
    output_dir = questionary.path("Path to output directory:").ask()
    link_distance = float(questionary.text(
        "link_distance:",
        validate=lambda v: v.replace(".", "").isdigit()
    ).ask())
    gaps = int(questionary.text(
        "gaps:",
        validate=lambda v: v.isdigit()
    ).ask())
    track_length = int(questionary.text(
        "track_length:",
        validate=lambda v: v.isdigit()
    ).ask())
    
    config = {
        "spots_file": os.path.relpath(spots_file, cwd),
        "output_dir": os.path.relpath(output_dir, cwd),
        "link_distance": link_distance,
        "gaps": gaps,
        "track_length": track_length
    }

    os.makedirs(output_dir, exist_ok=False)

    with open(os.path.join(cwd, "tracking_config.yaml"), "w") as f:
        yaml.safe_dump(config, f)


if __name__ == "__main__":
    build_config()