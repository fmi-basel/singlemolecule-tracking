## Extract single center slice from zstack for actin and tubulin intensities

Run task "iNeuron_single_slices".
```commandline
WD=runs/preprocessing/example pixi run iNeuron_single_slices
```

## Merging denoised and raw images for spot detection

To create dual channel images for spot detection run task "merge_raw_denoised_image".
```commandline
WD=runs/preprocessing/example pixi run merge_raw_denoised_image
```

## File renaming

For spot detection, the dual channel images and the cytoplasm masks have to have matching names, with the exception of "_ROIs" at the end of the mask images. To achieve that, run task "file_renaming" to change the name of the mask images. The names of the single slice images of the actin and tubulin channel created in task "iNeuron_single_slices" have to be changed accordingly as well.
```commandline
WD=runs/preprocessing/example pixi run file_renaming
```