All mask images need to be saved in tiff format (.tif).

## Manual mask creation with Fiji for organoid masks
This has to be done separately for whole cells and nuclei.

1. Open image with Fiji. Directories: "/"
1. Use `Freehand selections` tool to annotate ROI
1. Save as ImageJ `.roi` in zip file to be able to load all ROIs simultaneously later
1. Take single slice of image in one channel
1. Overlay ROIs
1. Convert ROIs to label image with `BIOP > Image Analysis > ROIs > ROIs to label image`
1. Change LUT to glasbey_inverted
1. Save label image (keep image name + extension "_ROIs").

Criteria for cytoplasm ROI selection:

1. Select cytoplasm that can be assigned to a nucleus (especially at early organoid development timepoints - at later timepoints, axons, whose nuclei are not in the FoV can also be selected).
1. Select cytoplasm of healthy cells (judged by intact nuclei).
1. Exclude nucleus.
1. Exclude obvious debris and dye accumlation (mostly from apoptotic/necrotic structures).

Note: Any other drawing tool (e.g. Napari) can be used alternatively to create matching whole cell and nucleus masks. 

After manual creation of whole cell and nucleus masks, run task "organoid_mask_creation" to substract nuclei from whole cells and create cytoplasm masks.
```commandline
WD=runs/mask_creation pixi run organoid_mask_creation
```

## Create max. intensity projections from zstack for iNeuron mask creation

Run task "iNeuron_zstack_processing".
```commandline
WD=runs/mask_creation pixi run iNeuron_zstack_processing
```

## Mask creation for iNeuron masks

1. For whole cell masks run task "iNeuron_cell_segmentation".
```commandline
WD=runs/mask_creation pixi run iNeuron_cell_segmentation
```
The script expects this folder structure:
```
Sample_experiment/
├── TreatmentFolder1/
│   ├── Max_projections_separate/
│   │   └── Halo/
│   │       └── *.tif
│   └── ROIs/
│       ├── Whole_cell/
│       └── Nucleus/
├── TreatmentFolder2/
│   ├── ...
...
```
The input path can either point to the whole experiment or to the specified sub-condition (treatment in this case).

1. For nuclei masks ilastik or any preferred segmentation tool can be used.
1. Correct nuclei masks and create cytoplasm masks with task "iNeuron_mask_creation".
```commandline
WD=runs/mask_creation pixi run iNeuron_mask_creation
```
1. Final masks can be manually corrected within the same notebook.

Alternative to steps 2-4:  Both nucleus and cytoplasm masks can be created by running task "iNeuron_mask_creation_with_nucleus".
```commandline
WD=runs/mask_creation pixi run iNeuron_mask_creation_with_nucleus
```
## Mask creation for iPSC masks

To segment cells and create masks for iPSC data run task "iPSC_mask_creation".
```commandline
WD=runs/mask_creation pixi run iPSC_mask_creation
```

## Mask creation for vascular progenitor masks

To segment cells and create masks for vascular progenitor data run task "vascular-progenitors_mask_creation".
```commandline
WD=runs/mask_creation pixi run vascular-progenitors_mask_creation
```
