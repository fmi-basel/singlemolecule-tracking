from multiprocessing import Pool
import os
from glob import glob
import pandas as pd
import numpy as np
import yaml

import trackpy as tp

from numpy.typing import ArrayLike

from tqdm import tqdm
import logging
from datetime import datetime

from os.path import join, basename

logger = logging.Logger('Tracking')
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
handler = logging.FileHandler(f"{now}-spot-detection.log") # How to replace?
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def load_data(spots_file: str):
    """Load file containig detected spots.
    
    Parameter:
        spots_file: Path to spots file.

    Returns:
        spots: Loaded spots file
    """
    spots = pd.read_csv(spots_file)

    return spots

def split_table_by_roi_id(spots: ArrayLike):
    """
    Splits each spots file into seperate dfs by roi-id, so that tracking can be done per ROI 
    """
    spots_per_ROI = [j for i,j in spots.groupby("roi_id", sort = False, as_index = False)]
    
    return spots_per_ROI

def linking(spots_per_ROI: list, linkdis: float, gaps: int, tracklen: int):
    """
    Links spots in dataframes with trackpy's basic linking function.

    Parameter:
        spots_per_ROI: list of spots per ROI

    Returns:
        tracks: DataFrame containing column 'Particle', representing linked particles
    """
   
    tracks_per_ROI = []

    for df in spots_per_ROI:
        df = tp.link(df, linkdis, memory = gaps)
        df = tp.filter_stubs(df, tracklen)
        tracks_per_ROI.append(df)
    
    tracks = pd.concat(tracks_per_ROI)

    return tracks

def create_track_id(row):
    """
    Funtion to create unique track-ids for all tracks of all ROIs per image by combining roi_id
    and particle number.
    """
    return f"{row['roi_id']}_{row['particle']}"

def apply_track_id(tracks: ArrayLike):
    """
    Creates track_id by ROI and particle number.
    Sorts values by track_id and frame.
    """
    tracks['track_id'] = tracks.apply(create_track_id, axis=1)
    tracks.index._name = 'index'
    tracks.sort_values(['track_id', 'frame'])

    return tracks

def uniqueid(tracks: ArrayLike):
    """
    Creates an additional column that contains unique track ids for easy visualization in Napari.    
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
            spots_file = spots_file,
            linkdis=config['linkdis'],
            gaps=config['gaps'],
            tracklen=config['tracklen']
        )

        name, _ = os.path.splitext(os.path.basename(spots_file))
        tracks_per_img.to_csv(os.path.join(config['output_dir'], f"{name}_tracks.csv"), index=False)

    logger.info("Done!")