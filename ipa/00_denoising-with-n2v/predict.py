from os.path import basename, splitext, join

import numpy as np
import yaml
from faim_ipa.utils import create_logger
from n2v.models import N2V
from tifffile import imread, imwrite

from config import N2VPredict
from generate_train_data_2D import list_images, move_axes_to_TZYXC

def main(config: N2VPredict):
    logger = create_logger("n2v-predict")
    logger.info(f"config: {config.dict()}")

    images = list_images(
        input_dir=config.input_dir,
        pattern=config.pattern
    )

    logger.info(f"Found {len(images)} images.")

    model = N2V(
        config=None,
        name=config.n2v_model_name,
        basedir=config.base_dir,
    )
    model.load_weights(f"weights_{config.weights}.h5")

    for file in images:
        logger.info(f"Predicting {file}.")
        name, ext = splitext(basename(file))
        data = imread(file)
        if "C" not in config.axes:
            data = data[..., np.newaxis]

        dtype = data.dtype

        data = move_axes_to_TZYXC(data, config.axes)
        if data.ndim == 5:
            pred = np.zeros_like(data)
            for t in range(data.shape[0]):
                for z in range(data.shape[1]):
                    pred[t, z] = np.clip(
                        model.predict(
                            img=data[t, z].astype(np.float32),
                            axes="YXC",
                        ),
                        np.iinfo(dtype).min,
                        np.iinfo(dtype).max,
                    ).astype(dtype)
        elif data.ndim == 4:
            pred = np.zeros_like(data)
            # Either z or t stack
            for s in range(data.shape[0]):
                pred[s] = np.clip(
                    model.predict(
                        img=data[s].astype(np.float32),
                        axes="YXC",
                    ),
                    np.iinfo(dtype).min,
                    np.iinfo(dtype).max,
                ).astype(dtype)
        elif data.ndim == 3:
            pred = np.clip(
                model.predict(
                    img=data.astype(np.float32),
                    axes="YXC",
                ),
                np.iinfo(dtype).min,
                np.iinfo(dtype).max,
            ).astype(dtype)

        pred = move_axes_from_TZYXC(pred, config.axes)

        if "C" not in config.axes:
            pred = pred[..., 0]

        imwrite(
            join(config.output_dir, name + "_denoised" + ext),
            pred,
        )

    logger.info("Done.")

def move_axes_from_TZYXC(data, axes: str):
    source, destination = (), ()
    i = 0
    for c in "TZYXC":
        if c in axes:
            source += (i,)
            destination += (axes.index(c),)
            i += 1

    return np.moveaxis(data, source, destination)


if __name__ == "__main__":
    with open("predict_config.yaml", "r") as f:
        config = N2VPredict(**yaml.safe_load(f))
        config.resolve_paths()

    main(config)