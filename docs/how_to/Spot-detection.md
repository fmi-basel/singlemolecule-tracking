For spot detection, dual channel images of the denoised (channel 1) and raw (channel 2 )images are necessary. Spot detection will be done on the denoised image and spot intensities will be extracted from the raw image at the determined xy coordinates.

Input parameters are:

1. (emission) wavelength: wavelength at which the fluorophore has its emission peak 

1. NA: numerical aperture of the objective

1. spacing: pixel sizes of the image in x and y

1. k: multiplication factor for hmax threshold 

For input requirements refer to the [spot_detection_script] (). k has to be empirically tested and depends on the dataset. For the available data set, threshold factors between 3 and 6 have been used.

## Spot detection without cytoskeletal stain intensities

For spot detection in organoid images run task "spot_detection".
```commandline
WD=runs/spot_detection/example pixi run spot_detection
```

## Spot detection with cytoskeletal stain intensities

For spot detection in iNeuron images, including extraction of cytoskeletal stains intensities, run task "spot_detection_cytoskeleton".
```commandline
WD=runs/spot_detection/example pixi run spot_detection_cytoskeleton
```

[Github](https://github.com/)