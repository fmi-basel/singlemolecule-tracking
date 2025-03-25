import os

import questionary
import yaml

from config import InputData, TrainModel, N2VPredict

GENERATE_TRAIN_DATA_CONFIG = "generate_train_data_config.yaml"
TRAIN_MODEL_CONFIG = "train_model_config.yaml"
PREDICT_CONFIG = "predict_config.yaml"


def configure_generate_train_data(existing_config: InputData = None) -> InputData:
    if existing_config is not None:
        existing_config.resolve_paths()

    input_dir = questionary.path(
        "Input directory:",
        default=str(existing_config.input_dir) if existing_config else "",
    ).ask()
    output_dir = questionary.path(
        "Output directory:",
        default=str(existing_config.output_dir) if existing_config else "",
    ).ask()
    pattern = questionary.text(
        "Pattern:",
        default=existing_config.pattern if existing_config else ".*.tif",
    ).ask()
    axes = questionary.text(
        "Axes:",
        default=existing_config.axes if existing_config else "ZYX",
    ).ask()
    xy_pixelsize_um = float(
        questionary.text(
            "XY pixelsize (um):",
            default=(
                str(existing_config.xy_pixelsize_um) if existing_config else "0.114"
            ),
            validate=lambda x: x.replace(".", "").isdigit(),
        ).ask()
    )
    patch_shape = tuple(
        int(x)
        for x in questionary.text(
            "Patch shape:",
            default=(
                ", ".join(map(str, existing_config.patch_shape))
                if existing_config
                else "128, 128"
            ),
            validate=lambda x: x.replace(" ", "").replace(",", "").isdigit(),
        )
        .ask()
        .split(",")
    )
    num_patches_per_img = int(
        questionary.text(
            "Number of patches per image:",
            default=(
                str(existing_config.num_patches_per_img) if existing_config else "8"
            ),
            validate=lambda x: x.isdigit(),
        ).ask()
    )

    return InputData(
        input_dir=input_dir,
        output_dir=output_dir,
        pattern=pattern,
        axes=axes,
        xy_pixelsize_um=xy_pixelsize_um,
        patch_shape=patch_shape,
        num_patches_per_img=num_patches_per_img,
    )


def configure_train_model(existing_config: TrainModel) -> TrainModel:
    train_data = questionary.path(
        "Train data:",
        default=str(existing_config.train_data) if existing_config else "",
    ).ask()
    val_data = questionary.path(
        "Validation data:",
        default=str(existing_config.val_data) if existing_config else "",
    ).ask()
    output_dir = questionary.path(
        "Output directory:",
        default=str(existing_config.output_dir) if existing_config else "",
    ).ask()
    n2v_model_name = questionary.text(
        "N2V model name:",
        default=existing_config.n2v_model_name if existing_config else "",
    ).ask()
    epochs = int(
        questionary.text(
            "Epochs:",
            default=str(existing_config.epochs) if existing_config else "200",
            validate=lambda x: x.isdigit(),
        ).ask()
    )
    batch_size = int(
        questionary.text(
            "Batch size:",
            default=str(existing_config.batch_size) if existing_config else "128",
            validate=lambda x: x.isdigit(),
        ).ask()
    )
    unet_depth = int(
        questionary.text(
            "Unet depth:",
            default=str(existing_config.unet_depth) if existing_config else "2",
            validate=lambda x: x.isdigit(),
        ).ask()
    )
    patch_shape = tuple(
        int(x)
        for x in questionary.text(
            "Patch shape:",
            default=(
                ", ".join(map(str, existing_config.patch_shape))
                if existing_config
                else "96, 96"
            ),
            validate=lambda x: x.replace(" ", "").replace(",", "").isdigit(),
        )
        .ask()
        .split(",")
    )

    return TrainModel(
        train_data=train_data,
        val_data=val_data,
        output_dir=output_dir,
        n2v_model_name=n2v_model_name,
        epochs=epochs,
        batch_size=batch_size,
        unet_depth=unet_depth,
        patch_shape=patch_shape,
    )


def configure_predict(existing_config: N2VPredict) -> N2VPredict:
    input_dir = questionary.path(
        "Input directory:",
        default=str(existing_config.input_dir) if existing_config else "",
    ).ask()
    output_dir = questionary.path(
        "Output directory:",
        default=str(existing_config.output_dir) if existing_config else "",
    ).ask()
    pattern = questionary.text(
        "Pattern:",
        default=existing_config.pattern if existing_config else ".*.stk",
    ).ask()
    axes = questionary.text(
        "Axes:",
        default=existing_config.axes if existing_config else "ZYX",
    ).ask()
    xy_pixelsize_um = float(
        questionary.text(
            "XY pixelsize (um):",
            default=(
                str(existing_config.xy_pixelsize_um) if existing_config else "0.114"
            ),
            validate=lambda x: x.replace(".", "").isdigit(),
        ).ask()
    )
    base_dir = questionary.path(
        "Base directory:",
        default=str(existing_config.base_dir) if existing_config else "",
    ).ask()
    n2v_model_name = questionary.text(
        "N2V model name:",
        default=existing_config.n2v_model_name if existing_config else "",
    ).ask()
    weights = questionary.text(
        "Weights:",
        default=existing_config.weights if existing_config else "last",
    ).ask()

    return N2VPredict(
        input_dir=input_dir,
        output_dir=output_dir,
        pattern=pattern,
        axes=axes,
        xy_pixelsize_um=xy_pixelsize_um,
        base_dir=base_dir,
        n2v_model_name=n2v_model_name,
        weights=weights,
    )


def main() -> None:

    create_config_for = questionary.checkbox(
        "Create config for:",
        choices=[
            "generate_train_data",
            "train_model",
            "predict",
        ],
    ).ask()

    if "generate_train_data" in create_config_for:
        generate_train_data = os.path.join(os.getcwd(), GENERATE_TRAIN_DATA_CONFIG)
        existing_config = None
        if os.path.exists(generate_train_data):
            with open(generate_train_data, "r") as f:
                existing_config = InputData(**yaml.safe_load(f))

        generate_train_data_config = configure_generate_train_data(existing_config)

        os.makedirs(generate_train_data_config.output_dir, exist_ok=True)

        generate_train_data_config.make_relative_paths()
        with open(generate_train_data, "w") as f:
            yaml.dump(generate_train_data_config.dict(), f)

    if "train_model" in create_config_for:
        train_model = os.path.join(os.getcwd(), TRAIN_MODEL_CONFIG)
        existing_config = None
        if os.path.exists(train_model):
            with open(train_model, "r") as f:
                existing_config = TrainModel(**yaml.safe_load(f))

        train_model_config = configure_train_model(existing_config)

        os.makedirs(train_model_config.output_dir, exist_ok=True)

        train_model_config.make_relative_paths()
        with open(train_model, "w") as f:
            yaml.dump(train_model_config.dict(), f)

    if "predict" in create_config_for:
        predict = os.path.join(os.getcwd(), PREDICT_CONFIG)
        existing_config = None
        if os.path.exists(predict):
            with open(predict, "r") as f:
                existing_config = N2VPredict(**yaml.safe_load(f))

        predict_config = configure_predict(existing_config)

        os.makedirs(predict_config.output_dir, exist_ok=True)
        predict_config.make_relative_paths()
        with open(predict, "w") as f:
            yaml.dump(predict_config.dict(), f)


if __name__ == "__main__":
    main()
