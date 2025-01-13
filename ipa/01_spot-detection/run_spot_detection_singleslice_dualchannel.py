from multiprocessing import Pool
import os
from glob import glob
from tifffile import imread
import pandas as pd
import numpy as np
from skimage.morphology import h_maxima, disk
from scipy.ndimage import gaussian_laplace
from skimage.util import img_as_float32, img_as_uint
import yaml
from spot_detection_utils import subpixel_localization_2d, get_spot

from numpy.typing import ArrayLike

from tqdm import tqdm
import logging
from datetime import datetime

from os.path import join, basename

# Setup logging
logger = logging.Logger('Spot Detection')
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
handler = logging.FileHandler(f"{now}-spot-detection.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def load_data(img_file: str, mask_file: str):
    """Load denoised and raw image from single-slice file."""
    img = imread(img_file)
    mask = imread(mask_file)

    # Channel mapping
    channel640 = img[1]  # Denoised channel
    channel561 = img[0]  # Raw channel

    return channel640, channel561, mask


def normalize_minmse(x, target):
    """Affine rescaling of x, such that the mean squared error to target is minimal."""
    cov = np.cov(x.flatten(), target.flatten())
    alpha = cov[0, 1] / (cov[0, 0] + 1e-10)
    beta = target.mean() - alpha * x.mean()
    return alpha * x + beta


def detect_spots(slice_img: ArrayLike, mask: ArrayLike, wavelength: int, NA: float, spacing: tuple[float, float], k: float):
    """Spot detection with LoG filter and h-maxima and std as threshold."""
    sigma = wavelength / (2 * NA) / np.sqrt(2) / (spacing[1] * 1000)
    log_img = -gaussian_laplace(img_as_float32(slice_img), sigma=sigma) * sigma**2
    log_img = img_as_uint(
        np.clip(
            normalize_minmse(log_img, img_as_float32(slice_img)),
            -1,
            1
        )
    )
    threshold = int(np.std(log_img[mask > 0])) * k
    spots = h_maxima(log_img, h=threshold, footprint=disk(int(sigma)))

    return spots * (mask > 0)


def assign_spots_to_ROIs(spots: ArrayLike, mask: ArrayLike):
    spots_per_roi = []
    roi_labels = list(filter(None, np.unique(mask)))

    for label_id in roi_labels:
        spots_per_roi.append(np.where(spots * (mask == label_id)))

    return spots_per_roi, roi_labels


def refine_spots(spots_per_roi: list, roi_labels: list, slice_img: ArrayLike, frame: int, logger: logging.Logger):
    subpix_spots = {}
    for roi_id, (y_coords, x_coords) in zip(roi_labels, spots_per_roi):
        subpix_spots[roi_id] = []
        for y, x in zip(y_coords, x_coords):
            spot_img, start_y, start_x = get_spot(slice_img, [y, x], size=5, logger=logger)
            try:
                bg, amp, x_loc, y_loc, sig_x, sig_y = subpixel_localization_2d(spot_img, spacing=(1, 1))
                subpix_spots[roi_id].append([start_y + y_loc, start_x + x_loc, bg, amp, sig_y, sig_x])
            except RuntimeError as e:
                logger.warning(e)
                logger.info(f"Skipped spot at {y, x}. Could not compute sub-pixel localization.")

    dfs = []
    for roi_id in subpix_spots:
        spot_df = pd.DataFrame(subpix_spots[roi_id], columns=['y', 'x', 'bg', 'amp', 'sigma_y', 'sigma_x'])
        spot_df['roi_id'] = roi_id
        spot_df['frame'] = frame

        dfs.append(spot_df)

    spots_for_frame_df = pd.concat(dfs, ignore_index=True)
    return spots_for_frame_df.reindex(columns=['frame', 'roi_id', 'x', 'y', 'bg', 'amp', 'sigma_y', 'sigma_x'])


def get_spot_intensity_computer(
        channel: ArrayLike,
):
    def spot_intensity_computer(row):
        y, x = row[['y', 'x']]
        y, x = int(np.round(y)), int(np.round(x))

        intensity = np.mean(channel[y - 1:y + 2, x - 1:x + 2])

        return intensity
    
    return spot_intensity_computer


def detect_spots_in_image(channel640: ArrayLike, channel561: ArrayLike, mask: ArrayLike, frame: int,
                          NA: float, wavelength: int, spacing: tuple[float, float], k: float):
    logger.info(f"Processing frame #{frame}.")
    spots = detect_spots(
        slice_img=channel640, 
        mask=mask, 
        NA=NA,
        wavelength=wavelength,
        spacing=spacing,
        k=k
    )

    spots_per_roi, roi_labels = assign_spots_to_ROIs(
        spots=spots, 
        mask=mask,
    )

    spots_for_frame_df = refine_spots(
        spots_per_roi=spots_per_roi,
        roi_labels=roi_labels,
        slice_img=channel640,
        frame=frame,
        logger=logger,
    )
    try:
        spots_for_frame_df['mean_intensity_channel640'] = spots_for_frame_df.apply(
            get_spot_intensity_computer(channel640), axis=1)
        spots_for_frame_df['mean_intensity_channel561'] = spots_for_frame_df.apply(
            get_spot_intensity_computer(channel561), axis=1)
    except ValueError as e:
        logger.warning("No spots in frame, skipping frame.")

    return spots_for_frame_df


def detect_spots_in_single_frame(img_file: str, mask_file: str,
                                 NA: float, wavelength: int, spacing: tuple[float, float], k: float):
    channel640, channel561, mask = load_data(
        img_file=img_file,
        mask_file=mask_file,
    )

    return detect_spots_in_image(
        channel640=channel640,
        channel561=channel561,
        mask=mask,
        frame=0,  # Single-slice
        NA=NA,
        wavelength=wavelength,
        spacing=spacing,
        k=k
    )


if __name__ == "__main__":
    with open("spot_detection_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Running spot-detection with config: {config}")

    img_files = glob(join(config['img_file'], '*.tif'))

    for img_file in tqdm(img_files):
        logger.info(f"Processing file: {img_file}")
        mask_file = join(config['mask_file'], basename(img_file).replace(".tif", "_ROIs.tif"))

        spots_for_frame = detect_spots_in_single_frame(
            img_file=img_file,
            mask_file=mask_file,
            NA=config['NA'],
            wavelength=config['wavelength'],
            spacing=config['spacing'],
            k=config['k']
        )

        name, _ = os.path.splitext(os.path.basename(img_file))
        spots_for_frame.to_csv(os.path.join(config['output_dir'], f"{name}_spots.csv"), index=False)

    logger.info("Done!")