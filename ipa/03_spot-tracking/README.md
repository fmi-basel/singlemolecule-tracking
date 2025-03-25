# Tracking with Trackpy

For reference see: http://soft-matter.github.io/trackpy/v0.6.1/

The run_tracking script uses the basic linking function of trackpy to link detected spots.

Parameters that have to be defined by the user:
1. link_distance: The maximum value in number of pixels that a particle can be displaced in xy between two frames to still be considered part of the same track.
2. gaps: For how many frames a particle can be missing to still be considered part of the same track.
3. track_length: The minimum number of frames in which a particle must be present to include the resulting track in the output, i.e., this parameter filters out short tracks.

Internally defined parameters are adaptive_stop and adaptive_step:
1. adaptive_stop: 2 pixels
2. adaptive_step: 0.95

They deal with cases when the subnetwork of particles is too large and they cannot be unambiguously assigned to one track, it reduces the network in a stepwise manner until it is able to resolve the network or the adaptive_stop threshhold is met. For reference see:
http://soft-matter.github.io/trackpy/v0.6.1/tutorial/adaptive-search.html

# Data availability

# Run tracking

1. Run tracking with task task "tracking".

To see the input parameters for tracking, check the log files for each run.
