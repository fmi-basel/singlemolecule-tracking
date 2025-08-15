## Calculating distance to nucleus

To only calculate the distance to the nucleus of each spot, run task "calculate_distance-to-nucleus".
```commandline
WD=runs/feature-extraction/example pixi run calculate_distance-to-nucleus
```
## Calculating distance to nucleus and creating cell compartment masks

Run task "cell_compartments" to calculate the distance to the nucleus and create masks of the cell compartments.
```commandline
WD=runs/feature-extraction/example pixi run cell_compartments
```
## Calculating distance to nucleus and cell edge

Run task "nuc_dist_edge_dist" to calculate the distance to the nucleus and the edge of the cell.
```commandline
WD=runs/feature-extraction/example pixi run nuc_dist_edge_dist
```