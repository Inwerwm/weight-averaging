import bpy

bl_info = {
    "name": "Weight Averaging",
    "author": "Inwerwm",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "",
    "description": "Averages the weights of the selected vertices.",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Rigging"
}


class INWERWM_OT_WeightAveraging(bpy.types.Operator):
    bl_idname: str = "rigging.weight_averaging.inwerwm"
    bl_label: str = "Average weights"
    bl_description: str = "Averages the weights of the selected vertices."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context):
        return {'FINISHED'}


def draw_menu(self, context):
    self.layout.separator()
    self.layout.operator(INWERWM_OT_WeightAveraging.bl_idname)


# Blender に登録するクラス
classes = [
    INWERWM_OT_WeightAveraging,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_mesh_add.append(draw_menu)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_menu)
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
