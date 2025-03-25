import pathlib

from faim_ipa.utils import resolve_with_git_root, make_relative_to_git_root
from pydantic import BaseModel, field_serializer


class InputData(BaseModel):
    input_dir: pathlib.Path
    output_dir: pathlib.Path
    pattern: str = "*.tif"
    axes: str = "ZYX"
    xy_pixelsize_um: float = 0.114
    patch_shape: list[int] = [128, 128]
    num_patches_per_img: int = 8

    @field_serializer("input_dir", "output_dir")
    def path_to_str(path: pathlib.Path):
        return str(path)

    def resolve_paths(self):
        if not self.input_dir.is_absolute():
            self.input_dir = resolve_with_git_root(self.input_dir)

        if not self.output_dir.is_absolute():
            self.output_dir = resolve_with_git_root(self.output_dir)

    def make_relative_paths(self):
        if self.input_dir.is_absolute():
            self.input_dir = make_relative_to_git_root(self.input_dir)

        if self.output_dir.is_absolute():
            self.output_dir = make_relative_to_git_root(self.output_dir)


class TrainModel(BaseModel):
    train_data: pathlib.Path
    val_data: pathlib.Path
    output_dir: pathlib.Path
    n2v_model_name: str
    epochs: int = 200
    batch_size: int = 128
    unet_depth: int = 2
    patch_shape: list[int] = [96, 96]

    @field_serializer("train_data", "val_data", "output_dir")
    def path_to_str(path: pathlib.Path):
        return str(path)

    def resolve_paths(self):
        if not self.train_data.is_absolute():
            self.train_data = resolve_with_git_root(self.train_data)

        if not self.val_data.is_absolute():
            self.val_data = resolve_with_git_root(self.val_data)

        if not self.output_dir.is_absolute():
            self.output_dir = resolve_with_git_root(self.output_dir)

    def make_relative_paths(self):
        if self.train_data.is_absolute():
            self.train_data = make_relative_to_git_root(self.train_data)

        if self.val_data.is_absolute():
            self.val_data = make_relative_to_git_root(self.val_data)

        if self.output_dir.is_absolute():
            self.output_dir = make_relative_to_git_root(self.output_dir)


class N2VPredict(BaseModel):
    input_dir: pathlib.Path
    output_dir: pathlib.Path
    pattern: str = "*.tif"
    axes: str = "ZYX"
    xy_pixelsize_um: float = 0.114
    base_dir: pathlib.Path
    n2v_model_name: str
    weights: str = "last"

    @field_serializer("input_dir", "output_dir", "base_dir")
    def path_to_str(path: pathlib.Path):
        return str(path)

    def resolve_paths(self):
        if not self.input_dir.is_absolute():
            self.input_dir = resolve_with_git_root(self.input_dir)

        if not self.output_dir.is_absolute():
            self.output_dir = resolve_with_git_root(self.output_dir)

        if not self.base_dir.is_absolute():
            self.base_dir = resolve_with_git_root(self.base_dir)

    def make_relative_paths(self):
        if self.input_dir.is_absolute():
            self.input_dir = make_relative_to_git_root(self.input_dir)

        if self.output_dir.is_absolute():
            self.output_dir = make_relative_to_git_root(self.output_dir)

        if self.base_dir.is_absolute():
            self.base_dir = make_relative_to_git_root(self.base_dir)
