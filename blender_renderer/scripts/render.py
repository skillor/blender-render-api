import bpy
import os
import json

# settings whitelist
RENDER_SETTINGS_SAVE_WHITELIST = [

    # cycles
    "cycles.adaptive_min_samples",
    "cycles.adaptive_threshold",
    "cycles.ao_bounces",
    "cycles.ao_bounces_render",
    "cycles.auto_scrambling_distance",
    "cycles.bake_type",
    "cycles.blur_glossy",
    "cycles.camera_cull_margin",
    "cycles.caustics_reflective",
    "cycles.caustics_refractive",
    "cycles.denoiser",
    "cycles.denoising_input_passes",
    "cycles.denoising_prefilter",
    "cycles.device",
    "cycles.dicing_rate",
    "cycles.diffuse_bounces",
    "cycles.direct_light_sampling_type",
    "cycles.distance_cull_margin",
    "cycles.fast_gi_method",
    "cycles.feature_set",
    "cycles.film_exposure",
    "cycles.film_transparent_glass",
    "cycles.film_transparent_roughness",
    "cycles.filter_width",
    "cycles.glossy_bounces",
    "cycles.light_sampling_threshold",
    "cycles.max_bounces",
    "cycles.max_subdivisions",
    "cycles.min_light_bounces",
    "cycles.min_transparent_bounces",
    "cycles.motion_blur_position",
    "cycles.name",
    "cycles.offscreen_dicing_scale",
    "cycles.pixel_filter_type",
    "cycles.rolling_shutter_duration",
    "cycles.rolling_shutter_type",
    "cycles.sample_clamp_direct",
    "cycles.sample_clamp_indirect",
    "cycles.sample_offset",
    "cycles.samples",
    "cycles.sampling_pattern",
    "cycles.scrambling_distance",
    "cycles.seed",
    "cycles.shading_system",
    "cycles.texture_limit",
    "cycles.texture_limit_render",
    "cycles.tile_size",
    "cycles.time_limit",
    "cycles.transmission_bounces",
    "cycles.transparent_max_bounces",
    "cycles.use_adaptive_sampling",
    "cycles.use_animated_seed",
    "cycles.use_auto_tile",
    "cycles.use_camera_cull",
    "cycles.use_denoising",
    "cycles.use_distance_cull",
    "cycles.use_fast_gi",
    "cycles.use_layer_samples",
    "cycles.volume_bounces",
    "cycles.volume_max_steps",
    "cycles.volume_step_rate",

    # render
    "render.bake_bias",
    "render.bake_margin",
    "render.bake_margin_type",
    "render.bake_samples",
    "render.bake_type",
    "render.bake_user_scale",
    "render.border_max_x",
    "render.border_max_y",
    "render.border_min_x",
    "render.border_min_y",
    "render.dither_intensity",
    "render.engine",
    "render.filepath",
    "render.film_transparent",
    "render.filter_size",
    "render.fps",
    "render.fps_base",
    "render.frame_map_new",
    "render.frame_map_old",
    "render.hair_subdiv",
    "render.hair_type",
    "render.line_thickness",
    "render.line_thickness_mode",
    "render.metadata_input",
    "render.motion_blur_shutter",
    "render.pixel_aspect_x",
    "render.pixel_aspect_y",
    "render.resolution_percentage",
    "render.resolution_x",
    "render.resolution_y",
    "render.simplify_child_particles",
    "render.simplify_child_particles_render",
    "render.simplify_gpencil",
    "render.simplify_gpencil_antialiasing",
    "render.simplify_gpencil_modifier",
    "render.simplify_gpencil_onplay",
    "render.simplify_gpencil_shader_fx",
    "render.simplify_gpencil_tint",
    "render.simplify_gpencil_view_fill",
    "render.simplify_subdivision",
    "render.simplify_subdivision_render",
    "render.simplify_volumes",
    "render.stamp_font_size",
    "render.stamp_note_text",
    "render.threads",
    "render.threads_mode",
    "render.use_bake_clear",
    "render.use_bake_lores_mesh",
    "render.use_bake_multires",
    "render.use_bake_selected_to_active",
    "render.use_bake_user_scale",
    "render.use_border",
    "render.use_compositing",
    "render.use_crop_to_border",
    "render.use_file_extension",
    "render.use_freestyle",
    "render.use_high_quality_normals",
    "render.use_lock_interface",
    "render.use_motion_blur",
    "render.use_multiview",
    "render.use_overwrite",
    "render.use_persistent_data",
    "render.use_placeholder",
    "render.use_render_cache",
    "render.use_sequencer",
    "render.use_sequencer_override_scene_strip",
    "render.use_simplify",
    "render.use_single_layer",
    "render.use_stamp",
    "render.use_stamp_camera",
    "render.use_stamp_date",
    "render.use_stamp_filename",
    "render.use_stamp_frame",
    "render.use_stamp_frame_range",
    "render.use_stamp_hostname",
    "render.use_stamp_labels",
    "render.use_stamp_lens",
    "render.use_stamp_marker",
    "render.use_stamp_memory",
    "render.use_stamp_note",
    "render.use_stamp_render_time",
    "render.use_stamp_scene",
    "render.use_stamp_sequencer_strip",
    "render.use_stamp_time",
    "render.views_format",

    # render.image_settings
    "render.image_settings.color_mode",
    "render.image_settings.file_format",
]


def blender_version():
    return ".".join([str(i) for i in bpy.app.version])

def apply_render_setting(scene, settings_key, render_settings):
    if settings_key in RENDER_SETTINGS_SAVE_WHITELIST:
        attribute = scene
        settings_key_split = settings_key.split('.')
        for attribute_part in settings_key_split[:-1]:
            if hasattr(attribute, attribute_part):
                attribute = getattr(attribute, attribute_part)
        last_part = settings_key_split[-1]
        last_attribute = getattr(attribute, last_part)
        setting_value = render_settings[settings_key]
        if isinstance(last_attribute, (bool, int, float, str, dict, list)) \
                and type(last_attribute) is type(setting_value):
            setattr(attribute, last_part, setting_value)


def apply_render_settings(scene, settings):
    if 'settings' not in settings:
        return
    render_settings = settings['settings']
    for settings_key in render_settings.keys():
        try:
            apply_render_setting(scene, settings_key, render_settings)
        except Exception as e:
            print(e)

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

with open('{$RENDER_SETTINGS_FILE}', 'r', encoding='utf8') as f:
    apply_render_settings(bpy.context.scene, json.loads(f.read()))

bpy.context.scene.render.filepath = '{$OUTPUT_FILE}'
bpy.ops.render.render(write_still=True)
