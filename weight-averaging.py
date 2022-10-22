import bpy
from bpy.props import EnumProperty

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
    "category": "Object",
}

word_map = {
    "en_US": {
        ("*", "Average Weights"): "Averaging",
        (
            "*",
            "Averages the weights of the selected vertices",
        ): "Averages the weights of the selected vertices",
        ("*", "Target Layers"): "Target Layers",
        ("*", "Target Layers Selection"): "Target Layers Selection",
        ("*", "All Layers"): "All Layers",
        ("*", "Averaging all data layers"): "Averaging all data layers",
        ("*", "Active Layer"): "Active Layer",
        ("*", "Only averaging active data layer"): "Only averaging active data layer",
        ("*", "There is no vertex groups"): "There is no vertex groups",
        (
            "*",
            "Verteices to be averaged is not selected",
        ): "Verteices to be averaged is not selected",
    },
    "ja_JP": {
        ("*", "Average Weights"): "平均化",
        ("*", "Averages the weights of the selected vertices"): "選択頂点のウェイトを平均化します",
        ("*", "Target Layers"): "対象レイヤー",
        ("*", "Target Layers Selection"): "複数のレイヤーがある場合、どのレイヤーを平均化するか",
        ("*", "All Layers"): "全レイヤー",
        ("*", "Averaging all data layers"): "全データレイヤーを平均化します",
        ("*", "Active Layer"): "アクティブレイヤー",
        ("*", "Only averaging active data layer"): "アクティブデータレイヤーのみ平均化します",
        ("*", "Verteices to be averaged is not selected"): "平均化対象頂点が選択されていません",
    },
}


class INWERWM_OT_WeightAveraging(bpy.types.Operator):
    bl_idname: str = "object.weight_averaging"
    bl_label: str = "Average Weights"
    bl_description: str = "Averages the weights of the selected vertices"
    bl_options = {"REGISTER", "UNDO"}

    target_layer: EnumProperty(
        name="Target Layers",
        description="Target Layers Selection",
        default="All",
        items=[
            ("All", "All Layers", "Averaging all data layers"),
            ("Active", "Active Layer", "Only averaging active data layer"),
        ],  # type: ignore
    )

    def execute(self, context: bpy.types.Context):
        # reflesh object data
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="EDIT")

        target_object = context.edit_object

        # load data of vertex groups
        vgroups = target_object.vertex_groups
        if len(vgroups) == 0:  # type: ignore
            self.report({"ERROR"}, "There is no vertex groups")
            return {"CANCELLED"}
        target_layers: list[bpy.types.VertexGroup] = (
            [vgroups.active] if self.target_layer == "Active" else [g for g in vgroups]  # type: ignore
        )

        weight_dict = {layer.index: 0.0 for layer in target_layers}

        # load selected vertices
        selected_vertices: list[bpy.types.MeshVertex] = [
            v for v in target_object.data.vertices if v.select  # type: ignore
        ]
        num_of_selected_vertices = len(selected_vertices)
        if num_of_selected_vertices < 2:
            self.report({"WARNING"}, "Verteices to be averaged is not selected")
            return {"CANCELLED"}

        # aggregate the weights for each vertex group
        for vertex in selected_vertices:
            for group in vertex.groups:
                if group.group in weight_dict.keys():
                    print(
                        f"vertex[{vertex.index}].groups[{str(group.group)}].weight += {group.weight}"
                    )
                    weight_dict[group.group] += group.weight

        for groupIndex in weight_dict:
            weight_dict[groupIndex] /= num_of_selected_vertices

        # update weights
        terget_indices = [v.index for v in selected_vertices]
        bpy.ops.object.mode_set(mode="OBJECT")
        for groupIndex in weight_dict:
            target_object.vertex_groups[groupIndex].add(
                terget_indices, weight_dict[groupIndex], "REPLACE"
            )
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}


def draw_menu(self, context):
    self.layout.separator()
    self.layout.operator(
        INWERWM_OT_WeightAveraging.bl_idname,
        text=bpy.app.translations.pgettext("Average Weights"),
    )


# Blender に登録するクラス
classes = [
    INWERWM_OT_WeightAveraging,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_edit_mesh_weights.append(draw_menu)
    bpy.app.translations.register(__name__, word_map)


def unregister():
    bpy.app.translations.unregister(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_weights.remove(draw_menu)
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
