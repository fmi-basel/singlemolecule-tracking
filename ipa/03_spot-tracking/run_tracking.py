import os
import argparse
import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import trackpy as tp
import yaml
from tqdm import tqdm


def setup_logger(log_dir: Path) -> logging.Logger:
    logger = logging.getLogger("Tracking")
    logger.setLevel(logging.INFO)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"{now}-spot-tracking.log"

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def split_table_by_roi_id(spots: pd.DataFrame):
    return [j for _, j in spots.groupby("roi_id", sort=False, as_index=False)]


def linking(spots_file: Path, link_distance: float, gaps: int, track_length: int):
    spots = pd.read_csv(spots_file)
    spots_per_roi = split_table_by_roi_id(spots)

    tracks_per_roi = []

    for df in spots_per_roi:
        df = tp.link(
            df, link_distance, memory=gaps, adaptive_stop=2, adaptive_step=0.95
        )
        df = tp.filter_stubs(df, track_length)
        tracks_per_roi.append(df)

    return pd.concat(tracks_per_roi)


def create_track_id(row: pd.Series) -> str:
    return f"{row['roi_id']}_{row['particle']}"


def add_track_id_column(tracks: pd.DataFrame) -> pd.DataFrame:
    # ✅ FIX: remove ambiguity between index + column
    tracks = tracks.reset_index(drop=True)

    tracks["track_id"] = tracks.apply(create_track_id, axis=1)
    tracks.sort_values(["track_id", "frame"], inplace=True)

    return tracks


def add_unique_id_column(tracks: pd.DataFrame) -> pd.DataFrame:
    tracks["unique_id"] = tracks["track_id"]
    track_ids = tracks["unique_id"].unique()

    tracks["unique_id"] = tracks["unique_id"].replace(
        to_replace=track_ids,
        value=np.random.permutation(len(track_ids)),
    )

    return tracks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", default=os.environ.get("WD", "."))
    args = parser.parse_args()

    workdir = Path(args.workdir).resolve()
    print("CWD:", os.getcwd())
    print("WORKDIR:", workdir)

    config_path = workdir / "tracking_config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with config_path.open("r") as f:
        config = yaml.safe_load(f)

    spots_dir = Path(config["spots_file"])
    output_dir = Path(config["output_dir"])

    output_dir.mkdir(parents=True, exist_ok=True)

    logger = setup_logger(workdir)
    logger.info(f"Running tracking with config: {config}")

    tp.ignore_logging()
    tp.logger = logger

    spots_files = list(spots_dir.glob("*.csv"))

    for spots_file in tqdm(spots_files):
        logger.info(f"Processing file: {spots_file}")

        tracks_per_img = linking(
            spots_file=spots_file,
            link_distance=config["link_distance"],
            gaps=config["gaps"],
            track_length=config["track_length"],
        )

        tracks_per_img = add_track_id_column(tracks_per_img)
        tracks_per_img = add_unique_id_column(tracks_per_img)

        output_file = output_dir / f"{spots_file.stem}_tracks.csv"
        tracks_per_img.to_csv(output_file, index=False)

    logger.info("Done!")