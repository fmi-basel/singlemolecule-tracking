# Predict Model

## Build Config

```commandline
WD=runs/example pixi run build_config
```
Navigate with the arrow keys to the task for which you want to build a config file and select it with the space key.

Input parameters to build the config file are:

1. axes: image axes, e.g., ZYX

2. base_dir: folder in which the trained models lie (parent directory of the model output folder)

3. n2v_model_name: name of the folder in which the training output of the specific model lies (child directory of the previous)

4. pattern: pattern of the image, e.g., .*.tif

5. weights: last - use the weights of the last epoch of the training, this can be changed to 'best'

6. xy_pixelsize_um: actual pixel sizes taking into account the magnification, e.g., 0.134 (um)


## Submit Job

### Option 1: Run it locally
```commandline
WD=runs/example pixi run predict
```

### Option 2: Run it on a cluster
```commandline
WD=runs/example JOB=predict ACCOUNT=account-name pixi run submit_job
```
Replace `account-name` with your cluster account name.
