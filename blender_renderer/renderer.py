import json
import os
import uuid
import subprocess
from typing import Dict, List, Any

from .cleaner import rm_dir


class Renderer:
    def __init__(self, blender_path: str, tmp_directory: str):
        self.blender_path = blender_path
        self.tmp_directory = tmp_directory

        scripts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts')

        with open(os.path.join(scripts_dir, 'get_texture_names.py'), 'r', encoding='utf8') as f:
            self.get_texture_names_template = f.read()

        with open(os.path.join(scripts_dir, 'get_render_settings.py'), 'r', encoding='utf8') as f:
            self.get_render_settings_template = f.read()

        with open(os.path.join(scripts_dir, 'render.py'), 'r', encoding='utf8') as f:
            self.render_template = f.read()

        with open(os.path.join(scripts_dir, 'unpack.py'), 'r', encoding='utf8') as f:
            self.unpack_template = f.read()

    @staticmethod
    def _prepare_template(template: str, replaces: Dict[str, str]) -> str:
        for key, value in replaces.items():
            template = template.replace(key, repr(str(value))[1:-1])
        return template

    def get_blender_command(self, scene_file_path, script_file_path):
        return [
            self.blender_path,
            scene_file_path,
            '--background',
            '--python', script_file_path,
            '--disable-autoexec',
        ]

    def get_texture_names(self, scene_bytes: bytes) -> List[str]:
        work_id = uuid.uuid4().hex

        working_dir = os.path.join(self.tmp_directory, work_id)

        image_names_file_path = os.path.join(working_dir, 'image_names.txt')

        script = self._prepare_template(self.get_texture_names_template, {
            '{$OUTPUT_FILE}': image_names_file_path
        })

        script_file_path = os.path.join(working_dir, 'script.py')

        os.makedirs(os.path.dirname(script_file_path), exist_ok=True)

        with open(script_file_path, 'w', encoding='utf8') as f:
            f.write(script)

        scene_file_path = os.path.join(working_dir, 'scene.blend')

        with open(scene_file_path, 'wb') as f:
            f.write(scene_bytes)

        command = self.get_blender_command(scene_file_path, script_file_path)

        result = subprocess.run(command,
                                shell=False,
                                cwd=working_dir,
                                env=dict(os.environ),
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                )

        if result.returncode != 0:
            rm_dir(working_dir)
            raise Exception('blender failed')

        with open(image_names_file_path, 'r', encoding='utf8') as f:
            texture_names = f.read().splitlines()

        rm_dir(working_dir)

        return texture_names

    def get_render_settings(self, scene_bytes: bytes) -> List[str]:
        work_id = uuid.uuid4().hex

        working_dir = os.path.join(self.tmp_directory, work_id)

        render_settings_file_path = os.path.join(working_dir, 'settings.json')

        script = self._prepare_template(self.get_render_settings_template, {
            '{$OUTPUT_FILE}': render_settings_file_path
        })

        script_file_path = os.path.join(working_dir, 'script.py')

        os.makedirs(os.path.dirname(script_file_path), exist_ok=True)

        with open(script_file_path, 'w', encoding='utf8') as f:
            f.write(script)

        scene_file_path = os.path.join(working_dir, 'scene.blend')

        with open(scene_file_path, 'wb') as f:
            f.write(scene_bytes)

        command = self.get_blender_command(scene_file_path, script_file_path)

        result = subprocess.run(command,
                                shell=False,
                                cwd=working_dir,
                                env=dict(os.environ),
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                )

        if result.returncode != 0:
            rm_dir(working_dir)
            raise Exception('blender failed')

        with open(render_settings_file_path, 'r', encoding='utf8') as f:
            render_settings = json.loads(f.read())

        rm_dir(working_dir)

        return render_settings

    def render(self,
               scene_bytes: bytes,
               textures: Dict[str, bytes] = None,
               render_settings: Dict[str, Any] = None,
               render_settings_string: str = None,
               render_settings_bytes: bytes = b'',
               ) -> bytes:
        if textures is None:
            textures = {}

        if render_settings is not None:
            render_settings_string = json.dumps(render_settings)

        if render_settings_string is not None:
            render_settings_bytes = render_settings_string.encode('utf8')

        work_id = uuid.uuid4().hex

        working_dir = os.path.join(self.tmp_directory, work_id)

        render_file_path = os.path.join(working_dir, 'render.png')

        render_settings_file_path = os.path.join(working_dir, 'settings.json')

        script = self._prepare_template(self.render_template, {
            '{$TMP_DIRECTORY}': working_dir,
            '{$OUTPUT_FILE}': render_file_path,
            '{$RENDER_SETTINGS_FILE}': render_settings_file_path,
        })

        script_file_path = os.path.join(working_dir, 'script.py')

        os.makedirs(os.path.dirname(script_file_path), exist_ok=True)

        with open(script_file_path, 'w', encoding='utf8') as f:
            f.write(script)

        with open(render_settings_file_path, 'wb') as f:
            f.write(render_settings_bytes)

        scene_file_path = os.path.join(working_dir, 'scene.blend')

        with open(scene_file_path, 'wb') as f:
            f.write(scene_bytes)

        for texture_name, image_bytes in textures.items():
            with open(os.path.join(working_dir, texture_name), 'wb') as f:
                f.write(image_bytes)

        command = self.get_blender_command(scene_file_path, script_file_path)

        result = subprocess.run(command,
                                shell=False,
                                cwd=working_dir,
                                env=dict(os.environ),
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                )

        if result.returncode != 0:
            rm_dir(working_dir)
            raise Exception('blender failed')

        with open(render_file_path, 'rb') as f:
            render_bytes = f.read()

        rm_dir(working_dir)

        return render_bytes

    def unpack(self,
               scene_bytes: bytes,
               ) -> Dict[str, bytes]:
        work_id = uuid.uuid4().hex

        working_dir = os.path.join(self.tmp_directory, work_id)

        texture_dir = os.path.join(working_dir, 'textures')

        script = self._prepare_template(self.unpack_template, {
            '{$TEXTURE_DIRECTORY}': texture_dir,
        })

        script_file_path = os.path.join(working_dir, 'script.py')

        os.makedirs(os.path.dirname(script_file_path), exist_ok=True)

        with open(script_file_path, 'w', encoding='utf8') as f:
            f.write(script)

        scene_file_path = os.path.join(working_dir, 'scene.blend')

        with open(scene_file_path, 'wb') as f:
            f.write(scene_bytes)

        command = self.get_blender_command(scene_file_path, script_file_path)

        result = subprocess.run(command,
                                shell=False,
                                cwd=working_dir,
                                env=dict(os.environ),
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                )

        if result.returncode != 0:
            rm_dir(working_dir)
            raise Exception('blender failed')

        texture_files = {}
        for texture_name in os.listdir(texture_dir):
            with open(os.path.join(texture_dir, texture_name), 'rb') as f:
                texture_files[texture_name] = f.read()

        rm_dir(working_dir)

        return texture_files
