import bpy
import os

for ob in bpy.data.objects:
    if ob.type == "MESH":
        for mat_slot in ob.material_slots:
            if mat_slot.material:
                if mat_slot.material.node_tree:
                    for x in mat_slot.material.node_tree.nodes:
                        if x.type == 'TEX_IMAGE':
                            image_name = str(x.image.name)
                            file_path = os.path.join('{$TEXTURE_DIRECTORY}', image_name)
                            image = bpy.data.images[image_name]
                            image.filepath = file_path
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            if image.packed_file is not None:
                                image.save()
