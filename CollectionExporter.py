bl_info= {
    "name": "Collection Exporter",
    "author": "YourName",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "Ctrl + E in Object Mode",
    "description": "Exports the collection of selected object as FBX",
    "category": "Import-Export",
} 


import bpy
import os

class CollectionExporter(bpy.types.Operator):
    bl_idname = "object.collection_exporter"
    bl_label = "Export Collection"

    def execute(self, context):
    
        obj = context.active_object

        if not obj:
            self.report({"ERROR"}, "No active object selected")
            return {'CANCELLED'}

        collections = obj.users_collection
        if not collections:
            self.report({"ERROR"}, "Object is not in any collection")
            return {'CANCELLED'}

        collection = collections[0]

        # self.report({"INFO"}, f"Collection: {collections.name}")


        for ob in collection.objects:
            ob.select_set(True)

        export_dir = bpy.path.abspath(context.scene.collection_exporter_props.export_path)
        export_path = os.path.join(export_dir, f"{collection.name}.fbx")
       
        
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        bpy.ops.export_scene.fbx(
            filepath=export_path,
            use_selection=True,
            apply_unit_scale=True,
            apply_scale_options="FBX_SCALE_ALL",
            bake_anim = False,
            use_mesh_modifiers=True,
            axis_forward = "-Z",
            axis_up ="Y"
            )

        obj.select_set(False)
        
        self.report({"INFO"}, f"Exported collection to: {export_path}")

        return {'FINISHED'}

class ExportCollectionPanel(bpy.types.Panel):
    bl_label = "Collection Exporter"
    bl_idname = "VIEW3D_PT_collection_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Collection Exporter"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Export Collection Panel")
        layout.label(text="Shortcut: Ctrl+E to Export")
        props = context.scene.collection_exporter_props
        layout.prop(props,"export_path")

class CollectionExporterProperties(bpy.types.PropertyGroup):
    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="Directory to save exported FBX",
        subtype='DIR_PATH',
        default="//"
    )


addon_keymaps = []


def register():

    bpy.utils.register_class(CollectionExporter) 

    bpy.utils.register_class(ExportCollectionPanel)

    bpy.utils.register_class(CollectionExporterProperties)
    bpy.types.Scene.collection_exporter_props = bpy.props.PointerProperty(type=CollectionExporterProperties)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name ="Object Mode", space_type="EMPTY")
    kmi = km.keymap_items.new(CollectionExporter.bl_idname, type="E", value="PRESS", ctrl=True)
    kmi.repeat = False
    addon_keymaps.append((km, kmi))

def unregister():
  
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    bpy.utils.unregister_class(CollectionExporter)

    bpy.utils.unregister_class(ExportCollectionPanel)

    del bpy.types.Scene.collection_exporter_props
    bpy.utils.unregister_class(CollectionExporterProperties)  

if __name__ == "__main__":
    register()