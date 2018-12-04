# d2line

## tubs_geo.py

Generate the code with description of d2 beamline.
For every pipe three lines are printed:
* `G4VSolid` defininition;
* `G4LogicalVolume` definition;
* place the logic volume `G4PVPlacement`.
The script uses beamtest2017B-tubs.tsv table.

Usage:
```bash
$ python tubs_geo.py
$ ./tubs_geo.py
$ ./tubs_geo.py z0 150.2
```


## S30400.cc

Stainless steel definition.
