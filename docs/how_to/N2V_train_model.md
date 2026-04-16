# Train Model

## Build Config

```commandline
WD=runs/denoising/config pixi run build_config
```
Navigate with the arrow keys to the task for which you want to build a config file and select it with the space key.

Input parameters to build the config file are:

1. batch_size: 128 - size of the previously defined patches

2. epochs: 200 - training epochs, this can be adapted

3. n2v_model_name: give your model a name - this will be the name of the folder that contains the training output

4. patch_shape: 96, 96 - 96 x 96 pixels, smaller than the extracted patches so that edge pixels have the same amount of neighbours as central pixels

5. train_data: training data as .npy file with the ending "x_train_2D" (output of the "generate_train_data" task)

6. unet_depth: 2 - depth of the unet used for training

7. val_data: validation data as .npy file with the ending "x_val_2D" (output of the "generate_train_data" task)


## Submit Job

### Option 1: Run it locally
```commandline
WD=runs/denoising/train pixi run train
```

### Option2: Run it on a cluster
```commandline
WD=runs/denoising/train JOB=train ACCOUNT=account-name pixi run submit_job
```
Replace `account-name` with your cluster account name.
