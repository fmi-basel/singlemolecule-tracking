# Manual mask creation with Fiji for organoid masks - has to be done separately for whole cells and nuclei

1. Open image with Fiji. Directories: "/"
1. Use `Freehand selections` tool to annotate ROI
1. Save as ImageJ `.roi` in zip file to be able to load all ROIs simultaneously later
1. Take single slice of image in one channel
1. Overlay ROIs
1. Convert ROIs to label image with `BIOP > Image Analysis > ROIs > ROIs to label image`
1. Change LUT to glasbey_inverted
1. Save label image (keep image name + extension) in a new directory called `ROIs_as_mask_BIOP`

Criteria for cytoplasm ROI selection:

1. Select cytoplasm that can be assigned to a nucleus (especially at early organoid development timepoints - at later timepoints, axons, whose nuclei are not in FoV can also be selected).
1. Select cytoplasm of healthy cells (judged by intact nuclei).
1. Exclude nucleus.
1. Exclude obvious debris and dye accumlation (mostly from apoptotic/necrotic structures).

After manual creation of whole cell and nucleus masks, run task "organoid_mask_creation" (how do I reference TASK here??) to substract nuclei from whole cells and create cytoplasm masks.

# Create max. intensity projections from zstack for mask creation

1. Run task "iNeuron_zstack_processing".

# Mask creation for iNeuron masks

1. For whole cell masks run task "iNeuron_cell_segmentation"
1. For nucleus mask use ilastik with model "MODEL". Parameters such as threshold sizes can be tuned manually if needed.
1. Correct nuclei masks and create and correct cytoplasm masks with task "iNeuron_mask_creation".

# Extract single center slice from zstack for actin and tubulin intensities

1. Run task "iNeuron_single_slices".

# Merging denoised and raw images for spot detection

1. To create dual channel images for spot detection run task "merge_raw_denoised_image".

# File renaming

1. For spot detection the dual channel images and the cytoplams mask have to have matching names, with the exception of "_ROIs" at the end of the mask images. To achieve that use the notebook from task "File_renaming" to change either the merged images or the masks (mask are recommended).

