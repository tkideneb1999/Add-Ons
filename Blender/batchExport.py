bl_info = {
    "name": "Batch Export",
    "blender": (3, 0, 0),
    "category": "Import-Export",
}

import bpy
from pathlib import Path

class VIEW3D_PT_BatchExport(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Batch Export"
    bl_label = "Settings"
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, 'batch_export_dir', text="Directory")
        layout.prop(context.scene, 'batch_export_coll', text="Collection")
        layout.operator('export.batch_export')


class EXPORT_OT_BatchExport(bpy.types.Operator):
    """batch export of Collection"""
    bl_idname = 'export.batch_export'
    bl_label = "Batch Export Collection"
    bl_options = {'REGISTER'}

    def execute(self, context):
        coll_name = context.scene.batch_export_coll
        export_dir = context.scene.batch_export_dir
        if export_dir == "":
            self.report({'ERROR'}, "Export Directory does not exist")
            return{'CANCELLED'}
        export_path = Path(bpy.path.abspath(export_dir))
        if not export_path.exists():
            self.report({'ERROR'}, f"Export Directory {str(export_path)} does not exist")
            return{'CANCELLED'}
        print(f"exporting collection: {coll_name}")
        print(f"Destination: {str(export_path)}")
        for coll in bpy.data.collections:
            if coll.name == coll_name:
                print("found export")
                for obj in coll.all_objects:
                    print(f"obj: {obj.name}")
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    
                    original_location = obj.location.copy()
                    print(original_location)
                    
                    obj_path = export_path / f"{obj.name}.fbx"
                    print(f"Object Path: {obj_path}")
                    
                    obj.location = [0.0, 0.0, 0.0]
                    bpy.ops.export_scene.fbx(filepath=str(obj_path), use_selection=True, apply_scale_options='FBX_SCALE_UNITS', bake_space_transform=True)
                    obj.location = original_location
                return {'FINISHED'}
        self.report({'ERROR'}, f"Collection {coll_name} does not exist")
        return{'CANCELLED'}

def register():
    bpy.types.Scene.batch_export_dir = bpy.props.StringProperty(
        name='Export Directory',
        subtype='DIR_PATH',
        default='//',
    )
    bpy.types.Scene.batch_export_coll = bpy.props.StringProperty(
        name='Export Collection',
        description="Collection to export",
    )
    bpy.utils.register_class(EXPORT_OT_BatchExport)
    bpy.utils.register_class(VIEW3D_PT_BatchExport)

def unregister():
    del bpy.types.Scene.batch_export_dir
    del bpy.types.Scene.batch_export_coll
    bpy.utils.unregister_class(EXPORT_OT_BatchExport)
    bpy.utils.unregister_class(VIEW3D_PT_BatchExport)