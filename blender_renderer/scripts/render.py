import bpy
import os

bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.image_settings.file_format = 'PNG'

for ob in bpy.data.objects:
    if ob.type == "MESH":
        for mat_slot in ob.material_slots:
            if mat_slot.material:
                if mat_slot.material.node_tree:
                    for x in mat_slot.material.node_tree.nodes:
                        if x.type == 'TEX_IMAGE':
                            image_name = str(x.image.name)
                            file_path = os.path.join('{$TMP_DIRECTORY}', image_name)
                            if os.path.isfile(file_path):
                                image = bpy.data.images[image_name]
                                image.filepath = file_path
                                if image.packed_file is not None:
                                    image.unpack()

bpy.context.scene.render.filepath = '{$OUTPUT_FILE}'
bpy.ops.render.render(write_still=True)
