# Blender Renderer Python

```bash
pip install blender-renderer
```

## Basic Usage
```python
from blender_renderer.renderer import Renderer

renderer = Renderer('blender.exe', 'tmp')

with open('scene.blend', 'rb') as f:
    scene_bytes = f.read()
texture_names = renderer.get_texture_names(scene_bytes)
print(texture_names)

with open('texture.png', 'rb') as f:
    texture_bytes = f.read()

texture_files_map = {
    'texture_name': texture_bytes,
}
    
img_bytes = renderer.render(
    scene_bytes,
    textures=texture_files_map,
)
```
