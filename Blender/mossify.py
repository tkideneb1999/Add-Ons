bl_info = {
    "name" : "Mossify",
    "blender" : (3, 1, 0),
    "category" : "Mesh"
}

import bpy

class MESH_OT_CreateMossLayers(bpy.types.Operator):
    """Create Moss Layers"""
    bl_idname = 'mesh.moss_create_layers'
    bl_label = "Create Moss Layers"
    bl_options = {'REGISTER', 'UNDO'}

    height: bpy.props.FloatProperty(
        name="Moss Height",
        description="Overall Height of the Moss",
        default=0.015,
        soft_min=0.0,
        soft_max=0.5
    )

    use_border: bpy.props.BoolProperty(
        name="Use Border Group",
        description="Enables option to have a different height for a specified Vertex Group",
        default=False
    )

    border_group: bpy.props.StringProperty(
        name="Border Group",
        description="Name of the Border Group",
        default="Border"
    )

    def execute(self, context):
        self.print("Generating Moss Layers:")
        self.print(f"Height: {self.height}")
        self.print(f"Use Border: {self.use_border}")
        self.print(f"Border Group: {self.border_group}")

        uv_offsets = [[-0.5, 0.0], [0.0, 0.5], [-0.5, 0.5]]

        initial_object_ID = context.active_object.name
        initial_object = bpy.data.objects[initial_object_ID]
        for i in range(3):
            bpy.ops.object.select_all(action='DESELECT')
            initial_object.select_set(True)
            context.view_layer.objects.active = initial_object
            bpy.ops.object.duplicate(linked=True)

            dupl_object = context.object
            dupl_object.parent = initial_object
            dupl_object.name = f"{initial_object_ID}_Layer{i+1}"
            dupl_object.location = [0.0, 0.0, 0.0]
            dupl_object.hide_select = True

            displ_mod = dupl_object.modifiers.new(name="MossDisplace", type='DISPLACE')
            displ_mod.mid_level=0.0
            displ_mod.strength = self.height / 3.0 * (i + 1)

            if self.use_border is True:
                has_vg_name = False
                for vg in dupl_object.vertex_groups:
                    if vg.name == self.border_group:
                        has_vg_name = True
                        break
                    else:
                        self.report({'INFO',
                                     f"[Mossify] Selected object has no Vertex Group named {self.border_group}"})
                if has_vg_name:
                    displ_mod.vertex_group = self.border_group

            uvwarp_mod = dupl_object.modifiers.new(name="MossUVWarp", type='UV_WARP')
            uvwarp_mod.offset = uv_offsets[i]

        initial_object.has_moss = True
        bpy.ops.object.select_all(action='DESELECT')
        context.view_layer.objects.active = initial_object
        initial_object.select_set(True)
        return {'FINISHED'}

    def print(self, msg):
        print(f"[{bl_info['name']}] " + str(msg))

class MESH_OT_MergeMossLayers(bpy.types.Operator):
    """Merge Moss Layers to Final Mesh"""
    bl_idname = 'mesh.moss_merge_layers'
    bl_label = "MergeMossLayers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_object_name = context.active_object.name
        selected_object = bpy.data.objects[selected_object_name]
        if selected_object.has_moss is False:
            self.report({'INFO', f"[Mossify] Selected Object is no Moss"})
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')
        selected_object.select_set(True)
        for c in selected_object.children:
            c.hide_select = False
            c.select_set(True)
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', obdata=True)

        for c in selected_object.children:
            context.view_layer.objects.active = c
            bpy.ops.object.modifier_apply(modifier="MossDisplace")
            bpy.ops.object.modifier_apply(modifier="MossUVWarp")

        bpy.ops.object.select_all(action='DESELECT')
        selected_object.select_set(True)
        for c in selected_object.children:
            c.select_set(True)
        context.view_layer.objects.active = selected_object
        bpy.ops.object.join()

        return {'FINISHED'}

def register():
    bpy.types.Object.has_moss = bpy.props.BoolProperty(
        name="Has Moss",
        default=False,
        options={'HIDDEN'}
    )
    bpy.utils.register_class(MESH_OT_CreateMossLayers)
    bpy.utils.register_class(MESH_OT_MergeMossLayers)

def unregister():
    del bpy.types.Object.has_moss
    bpy.utils.register_class(MESH_OT_MergeMossLayers)
    bpy.utils.unregister_class(MESH_OT_CreateMossLayers)