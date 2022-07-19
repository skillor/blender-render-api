import bpy
import os

texture_names = set()
for ob in bpy.data.objects:
    if ob.type == "MESH":
        for mat_slot in ob.material_slots:
            if mat_slot.material:
                if mat_slot.material.node_tree:
                    for x in mat_slot.material.node_tree.nodes:
                        if x.type == 'TEX_IMAGE':
                            texture_names.add(str(x.image.name))

output_file = '{$OUTPUT_FILE}'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w', encoding='utf8') as f:
    f.write('\n'.join(texture_names))
