# Manual ROI selection with Fiji

1. Open image with Fiji
1. Use `Freehand selections` tool to annotate ROI
1. Save as ImageJ `.roi` in zip file to be able to load all ROIs simultaneously later
1. Take single slice of image in one channel
1. Overlay ROIs
1. Convert ROIs to label image with `BIOP > Image Analysis > ROIs > ROIs to label image`
1. Change LUT to glasbey_inverted
1. Save label image (keep image name + extension) in a new directory next to the images called `ROIs_as_mask_BIOP`

Criteria for ROI selection:

1. Select cytoplasm that can be assigned to a nucleus (especially at early organoid development timepoints - at later timepoints, axons, whose nuclei are not in FoV can also be selected).
1. Select cytoplasm of healthy cells (judged by intact nuclei).
1. Exclude nucleus.
1. Exclude obvious debris and dye accumlation (mostly from apoptotic/necrotic structures).

