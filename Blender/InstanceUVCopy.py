bl_info = {
    "name": "Instance UV Copy",
    "blender": (3, 1, 0),
    "category": "Geometry Nodes",
    "description": "Copies UV Information from Instanced Objects in Geo Nodes to UV Map"
}

import bpy

class MESH_OT_CopyInstanceUVs(bpy.types.Operator):
    """Copy UV of Instanced Geo Nodes Objects"""
    bl_idname = 'mesh.copy_instance_uvs'
    bl_label = "Copy Instance UVs"
    bl_options = {'REGISTER', 'UNDO'}
    
    uv_map_name: bpy.props.StringProperty(
        name="UV Map",
        default="UVMap"
    )
    
    def execute(self, context):
        target = context.active_object

        if target.data.attributes.get(self.uv_map_name) is None:
            print(f"No Attribute UV Map named {self.uv_map_name}")
            return {'CANCELLED'}
        elif len(target.data.uv_layers) <= 0:
            print(f"No UV Map exists! Creating one")
            target.data.uv_layers.new(name=self.uv_map_name)
        attrUV = target.data.attributes[self.uv_map_name].data
        targetUV = target.data.uv_layers[0].data

        for i, elem in enumerate(targetUV):
            elem.uv = attrUV[i].vector
        
        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(MESH_OT_CopyInstanceUVs)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_CopyInstanceUVs)