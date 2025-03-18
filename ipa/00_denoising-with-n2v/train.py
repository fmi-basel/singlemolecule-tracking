import numpy as np
import yaml
from faim_ipa.utils import create_logger
from n2v.models import N2V, N2VConfig

from config import TrainModel

def train_model(
    config: TrainModel,
):
    logger = create_logger("train-n2v")
    logger.info(f"config: {config.dict()}")

    x = np.load(config.train_data)
    x_val = np.load(config.val_data)
    print(x.shape)
    n2v_config = N2VConfig(
        x,
        unet_n_depth=config.unet_depth,
        unet_kern_size=3,
        unet_residual=False,
        train_steps_per_epoch=int(x.shape[0] / config.batch_size),
        train_epochs=config.epochs,
        train_loss="mse",
        batch_norm=True,
        train_batch_size=config.batch_size,
        n2v_perc_pix=0.198,
        n2v_patch_shape=tuple(config.patch_shape),
        n2v_manipulator="median",
        blurpool=True,
        skip_skipone=True,
        n2v_neighborhood_radius=2,
    )

    model = N2V(
        config=n2v_config,
        name=config.n2v_model_name,
        basedir=config.output_dir,
    )

    logger.info(f"model: {model}")

    model.train(x, x_val)

    logger.info("Done.")

if __name__ == "__main__":
    with open("train_model_config.yaml", "r") as f:
        config = TrainModel(**yaml.safe_load(f))
        config.resolve_paths()

    train_model(config)
