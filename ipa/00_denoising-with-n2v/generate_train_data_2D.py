import os
import pathlib
import re
from copy import copy
from os.path import join
import random

import yaml
from n2v.internals.N2V_DataGenerator import N2V_DataGenerator
from tifffile import imread

from config import InputData
import numpy as np
from faim_ipa.utils import create_logger


def generate_train_data_2D(
    config: InputData,
) -> None:

    logger = create_logger("generate-train-data-2D")
    logger.info(f"config: {config.dict()}")

    img_files = list_images(
        input_dir=config.input_dir,
        pattern=config.pattern,
    )

    logger.info(f"Found {len(img_files)} images.")

    assert (
        len(img_files) >= 2
    ), "Require at least two images to generate train and validation data."

    img_files_shuffled = copy(img_files)
    random.shuffle(img_files_shuffled)
    datagen = N2V_DataGenerator()
    split = int(min(max(len(img_files) * 0.1, 1), 500))
    images = []
    for file in img_files_shuffled:
        data = imread(file)

        assert data.ndim <= 5, "Data can have at most 5 dimensions: TZYXC"

        data = move_axes_to_TZYXC(data, config.axes)

        if "C" in config.axes:
            assert (
                data.shape[config.axes.index("C")] == 1
            ), "Only single channel images are supported."

        if "T" in config.axes and "Z" in config.axes:
            data = np.concatenate(data, axis=0)

        if data.ndim == 2:
            data = data[np.newaxis, ..., np.newaxis]

        if data.ndim == 3:
            data = data[..., np.newaxis]

        images.append(data)

    logger.info(f"Using {split} number of images for validation.")
    x_val_data = datagen.generate_patches_from_list(
        images[:split],
        num_patches_per_img=config.num_patches_per_img,
        shape=config.patch_shape,
        augment=False,
    )
    logger.info(f"Using {len(images) - split} number of images for training.")
    x_train_data = datagen.generate_patches_from_list(
        images[split:],
        num_patches_per_img=config.num_patches_per_img,
        shape=config.patch_shape,
        augment=True,
    )
    val_output_file = join(config.output_dir, "x_val_2D.npy")
    np.save(val_output_file, x_val_data)
    logger.info(f"Saved validation data to {val_output_file}.")
    train_output_file = join(config.output_dir, "x_train_2D.npy")
    np.save(train_output_file, x_train_data)
    logger.info(f"Saved training data to {train_output_file}.")

    logger.info("Done.")


def list_images(
    input_dir: pathlib.Path,
    pattern: str,
) -> list[str]:
    pattern_re = re.compile(pattern)
    images = []
    for entry in os.scandir(input_dir):
        if entry.is_file():
            if pattern_re.fullmatch(entry.name):
                images.append(entry.path)

    return images


def move_axes_to_TZYXC(data, axes: str):
    source, destination = (), ()
    i = 0
    for c in "TZYXC":
        if c in axes:
            source += (axes.index(c),)
            destination += (i,)
            i += 1

    return np.moveaxis(data, source, destination)


if __name__ == "__main__":

    with open("generate_train_data_config.yaml", "r") as f:
        config = InputData(**yaml.safe_load(f))
        config.resolve_paths()

    generate_train_data_2D(
        config=config,
    )
