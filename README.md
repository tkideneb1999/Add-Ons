# Add-Ons
This is a collection of various small Add-Ons
## Blender
### Batch Export
This Add-On exports a collection as single objects in the fbx format. It applys the FBX Units Scale and the Transform. The user has to type in a collection and set a directory where to put the objects.
### Mossify
Mossify implements two new operators that allow for fast layered moss mesh creation as described in this [article](https://docs.cryengine.com/display/SDKDOC2/How+to+Create+Layered+Moss) in the CryEngine Wiki
#### Usage
1. Create the initial moss patch
2. UV Unwrap the patch and scale it down by 0.5, then putting it in the lower right quarter.
3. (optional) Create a vertex group defining the per vertex distance between the individual layers. This can be used to minimize the distance around the edges of the moss mesh
4. Use the "Create Moss Layers" Operator accessible via the F3 Search bar. Here the moss height can be adjusted as well as whether to use a group for the per vertex strength. This creates 3 additional instanced copies and parents them under the initial mesh and makes them not selectable in the viewport. You can still adjust the individual positions of the vertices as well as the UVs.
5. Use the "Merge Moss Layers" Operator after finishing the moss layer adjustment. This merges all four meshes created by the previous Operator.
6. Lastly, the mesh can be exported.
### Instance UV Copy
A simple script to fix the UVs of Geometry Node Meshes that instance objects.

After applying the geometry nodes modifier, the Add-On converts the UVs from the Attribute to a specified UV Map. If none exists one is created.
