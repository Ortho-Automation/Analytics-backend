# Preparing data

## Data provided

- Open_Pit_Mine.glb
- Metadata.json

Need to perform rotate y 90 then z 90

- 3d_model .glb

Corrected rotation

## Github Data

- BoxAnimated.glb
- BoxAnimated.json

## GLB > OBJ > PLY > OBJ Data

1. Convert `3d_model .glb` to ImageTOStl.com obj files using the website
2. Open CloudCompare window software and imported converted obj.
3. Exported it as `ccascii2.ply` as we wanted to extract colors
4. Finally, using `Scripts/extractobjfromply.py`, we write the colors back to the obj without the uses of `mtl` data format.

## PLY > XYZ

1. To get color information better follow previous stage.
2. Use online converter to convert glb to obj which is human readable.
3. Extract the xyz information using `Scipts/extractxyzfromply.py`.

## JSON files

- Json files store coordinate information for meshes and point clouds.
- The coordinates act as real world origin of the center of 3D model.
- They are recommended when uploading, its optional if you want to define your coordinate on frontend.