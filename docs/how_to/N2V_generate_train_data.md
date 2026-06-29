# Generate Training Data

## Build Config

```commandline
pixi run build_config
```
Navigate with the arrow keys to the task for which you want to build a config file and select it with the space key.
Input parameters to build the config file are:

1. axes: image axes, e.g., ZYX

2. num_patches_per_img: 8 - 8 patches per image are extracted, this can be changed depending on the amount of training data

3. patch_shape: 128, 128 - 128 x 128 pixels, this area needs to be larger than the patch on which the actual training is performed, so that edge pixels have the same amount of neighbours as central pixels

4. pattern: pattern of the image, e.g., .*.tif

5. xy_pixelsize_um: actual pixel sizes taking into account the magnification, e.g., 0.134 (um)


## Submit Job

### Option 1: Run it locally
```commandline
pixi run generate_data
```

### Option 2: Run it on a cluster
```commandline
WD=runs/denoising/generate JOB=generate_data ACCOUNT=account-name pixi run submit_job
```
Replace `account-name` with your cluster account name.
