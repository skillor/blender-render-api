import bpy
import os

bpy.context.scene.render.resolution_x = int('{$RESOLUTION_X}')
bpy.context.scene.render.resolution_y = int('{$RESOLUTION_Y}')
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
                            bpy.data.images[str(x.image.name)].filepath = os.path.join('{$TMP_DIRECTORY}',
                                                                                       str(x.image.name))

bpy.context.scene.render.engine = 'BLENDER_EEVEE'
for scene in bpy.data.scenes:
    scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.filepath = '{$OUTPUT_FILE}'
bpy.ops.render.render(write_still=True)
