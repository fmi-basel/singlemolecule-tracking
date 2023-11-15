import logging
import os
from datetime import datetime
from glob import glob
from os.path import join

import numpy as np
import pandas as pd
import trackpy as tp
import yaml
from numpy._typing import ArrayLike
from tqdm import tqdm

logger = logging.Logger('Tracking')
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
handler = logging.FileHandler(f"{now}-spot-tracking.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def split_table_by_roi_id(spots: pd.DataFrame) -> list[pd.DataFrame]:
    """
    Splits each spots file into seperate dfs by roi-id, so that tracking can
    be done per ROI.

    Parameter:
        spots: DataFrame containing spots

    Returns:
        spots_per_ROI: List of DataFrames containing spots per ROI
    """
    return [j for i,j in spots.groupby("roi_id", sort = False, as_index = False)]


def linking(
    spots_file: str,
    link_distance: float,
    gaps: int,
    track_length: int
):
    """
    Links spots in dataframes with trackpy's basic linking function.

    Parameter:
        spots_file: path to spots file
        link_distance: maximum distance between two spots to be linked
        gaps: maximum number of frames a spot can be missing
        track_length: minimum length of track to be included in the output

    Returns:
        tracks: DataFrame containing column 'Particle', representing linked particles
    """
    spots = pd.read_csv(spots_file)
    spots_per_roi = split_table_by_roi_id(spots)
   
    tracks_per_roi = []

    for df in spots_per_roi:
        df = tp.link(df, link_distance, memory=gaps)
        df = tp.filter_stubs(df, track_length)
        tracks_per_roi.append(df)
    
    return pd.concat(tracks_per_roi)


def create_track_id(row: pd.Series) -> str:
    """
    Funtion to create unique track-ids for all tracks of all ROIs per image by combining roi_id
    and particle number.
    """
    return f"{row['roi_id']}_{row['particle']}"


def add_track_id_column(tracks: pd.DataFrame) -> pd.DataFrame:
    """
    Creates track_id by ROI and particle number.
    Sorts values by track_id and frame.

    Parameter:
        tracks: DataFrame containing tracks

    Returns:
        tracks: DataFrame containing tracks with track_id column
    """
    tracks['track_id'] = tracks.apply(create_track_id, axis=1)
    tracks.index._name = 'index'
    tracks.sort_values(['track_id', 'frame'])

    return tracks


def add_unique_id_column(tracks: pd.DataFrame) -> pd.DataFrame:
    """
    Creates an additional column that contains unique track ids for easy visualization in Napari.

    Parameter:
        tracks: DataFrame containing tracks

    Returns:
        tracks: DataFrame containing tracks with unique_id column
    """
    tracks['unique_id'] = tracks['track_id']
    track_ids = tracks['unique_id'].unique()
    tracks['unique_id'] = tracks['unique_id'].replace(to_replace=track_ids, value=np.random.permutation(len(track_ids)))

    return tracks


if __name__ == "__main__":
    with open("tracking_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Running tracking with config: {config}")

    spots_files = glob(join(config['spots_file'], '*.csv'))

    for spots_file in tqdm(spots_files):
        logger.info(f"Processing file: {spots_file}")

        tracks_per_img = linking(
            spots_file=spots_file,
            link_distance=config['linkdis'],
            gaps=config['gaps'],
            track_length=config['tracklen']
        )

        tracks_per_img = add_track_id_column(tracks_per_img)

        tracks_per_img = add_unique_id_column(tracks_per_img)

        name, _ = os.path.splitext(os.path.basename(spots_file))
        tracks_per_img.to_csv(join(config['output_dir'], f"{name}_tracks.csv"), index=False)

    logger.info("Done!")
