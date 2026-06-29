# Tracking with Trackpy

For reference see: [Trackpy](http://soft-matter.github.io/trackpy/v0.6.1/)

The tracking script uses the basic linking function of trackpy to link detected spots.

Parameters that have to be defined by the user:

1. link_distance: The maximum value in number of pixels that a particle can be displaced in xy between two frames to still be considered part of the same track.

1. gaps: For how many frames a particle can be missing to still be considered part of the same track.

1. track_length: The minimum number of frames in which a particle must be present to include the resulting track in the output, i.e., this parameter filters out short tracks.

The parameters have to be tested empirically and depend on the dataset. For the available dataset linking distances of 5 (50ms dataset) and 7 (500ms dataset) have been used. Allowed gaps were 2 and minimum track length 5.


## Run tracking

Run tracking with task task "tracking". Output folder needs to be created while building the config file.
```commandline
WD=runs/tracking pixi run tracking
```
