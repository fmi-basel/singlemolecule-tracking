from tifffile import imread
from skimage.morphology import disk
from matplotlib.colors import ListedColormap
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from skimage.morphology import h_maxima
from skimage.measure import regionprops
from spot_detection_utils import subpixel_localization, get_spot



def main(file, file2, frame):
    image = imread(file)
    mask = imread(file2)
    
    # TODO: Add functionality from spot_detection.ipynb

    denoised_img = image[:, 0]
    raw_img = image[:, 1]
    plt.imshow(mask > 0)

    # Mask out foreground (mask > 0) --> go from instance segmentation to semantic segmentation (fg vs bg)
    masked_cells = denoised_img * (mask > 0)

    plt.figure(figsize=(10,10))
    plt.imshow(masked_cells[frame], cmap='gray')

    # H-max spot detection with std as threshold

    threshold = int(np.std(denoised_img[frame, mask > 0]))
    spots = h_maxima(image=denoised_img[frame], footprint=disk(1), h=threshold)
    spots = spots * (mask > 0)
    
    spot_cmap = ListedColormap([[0, 0, 0, 0], [1, 0, 0, 1]])
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1,2,1)
    plt.imshow(masked_cells[frame], cmap='gray')
    plt.subplot(1,2,2)
    plt.imshow(masked_cells[frame], cmap='gray')
    plt.imshow(spots, cmap=spot_cmap)

    # Assign spots to ROIs
    spots_per_roi = []
    roi_labels = list(filter(None, np.unique(mask)))

    for label_id in roi_labels:
        spots_per_roi.append(np.where(spots * (mask == label_id)))
        

    # subpixel localization of spots and visualization
    spot_size = 3

    subpix_spots = {}
    for roi_id, (y_coords, x_coords) in zip(roi_labels, spots_per_roi):
        subpix_spots[roi_id] = []
        for y, x in zip(y_coords, x_coords):
            spot_img, start_y, start_x = get_spot(denoised_img[frame], [y, x], size=5)
            y_loc, x_loc = subpixel_localization(spot_img)
            subpix_spots[roi_id].append([start_y + y_loc, start_x + x_loc])
    
    features = regionprops(mask)

    # Overlay subpixel localized spots on raw image frame.
    marker_style = dict(color='tab:red', linestyle=':', marker='o',
                        markersize=15, markerfacecoloralt='tab:red')

    for prop in features:
        box = prop.bbox
        plt.imshow((raw_img[frame] * (mask == prop.label))[box[0]:box[2], box[1]:box[3]])
        for y, x in subpix_spots[prop.label]:
            plt.plot(x - box[1], y- box[0], fillstyle='none', **marker_style)

        plt.title(f'ROI {prop.label}')
        plt.show()

    dfs = []
    for roi_id in subpix_spots:
        spot_df = pd.DataFrame(subpix_spots[roi_id], columns=['y', 'x'])
        spot_df['roi_id'] = roi_id
        spot_df['frame'] = frame

        dfs.append(spot_df)

    spots_for_frame_df = pd.concat(dfs, ignore_index=True)
    spots_for_frame_df = spots_for_frame_df.reindex(columns=['frame', 'roi_id', 'x', 'y'])

    return spots_for_frame_df

def import_images(file1, file2):
    """Imports merged denoised and raw image (file1) and ROI mask (file2)"""
    image = imread(file)
    mask = imread(file2)
    denoised_img = image[:, 0]
    raw_img = image[:, 1]
    plt.imshow(mask > 0)
    return image, mask


def get_masked_cells(denoised_img, mask):
    """Mask out foreground (mask > 0) --> go from instance segmentation to semantic segmentation (fg vs bg)"""
    masked_cells = denoised_img * (mask > 0)
    plt.figure(figsize=(10,10))
    plt.imshow(masked_cells[frame], cmap='gray')
    return masked_cells

def h-max_spot_detec






if __name__ == "__main__":
    main(
        file = '/Volumes/gchao/bamfaile/Analysis/TUBB2B-KI/Batch20230223/D21/Denoised/100tp_561-100-50ms-1000g_4_conf561_merged.tif',
        file2 = '/Volumes/gchao/bamfaile/Analysis/TUBB2B-KI/Batch20230223/D21/ROIs/ROIs_as_mask_BIOP/100tp_561-100-50ms-1000g_4_conf561_merged_ROI1-18.tif',
        frame = 10,
           )