"""Save an untouched Blender stage copy and render four orthographic clay views.

Run with: blender --background scene.blend --python-exit-code 1 --python stage_review.py --
          --stage blockout --output /path/to/reviews [--object MeshName]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import bpy
from mathutils import Vector


VIEWS = {
    "front": (0.0, -1.0, 0.0),
    "three_quarter": (1.0, -1.0, 0.15),
    "profile": (1.0, 0.0, 0.0),
    "back": (0.0, 1.0, 0.0),
}


def arguments():
    user_args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, help="New checkpoint name, e.g. blockout or primary-v2")
    parser.add_argument("--output", required=True, help="Parent directory for review stages")
    parser.add_argument("--object", help="Review one named mesh; otherwise use visible mesh objects")
    parser.add_argument("--resolution", type=int, default=512)
    args = parser.parse_args(user_args)
    if not re.fullmatch(r"[a-z][a-z0-9_-]{0,39}", args.stage):
        parser.error("--stage must start with a lowercase letter and contain only a-z, 0-9, _ or -")
    if not 64 <= args.resolution <= 4096:
        parser.error("--resolution must be 64..4096")
    return args


def selected_meshes(name):
    if name:
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != "MESH":
            raise ValueError(f"Mesh object not found: {name}")
        return [obj]
    objs = [obj for obj in bpy.context.scene.objects if obj.type == "MESH" and obj.visible_get()]
    if not objs:
        raise ValueError("No visible mesh objects in the scene")
    return objs


def world_bounds(objs):
    points = [obj.matrix_world @ Vector(corner) for obj in objs for corner in obj.bound_box]
    low = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    high = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    center = (low + high) / 2
    span = max(high[i] - low[i] for i in range(3))
    if span <= 0:
        raise ValueError("Selected mesh bounds have zero extent")
    return center, span, low, high


def render_views(stage_dir, objs, center, span, resolution):
    scene = bpy.context.scene
    selected = set(objs)
    for obj in scene.objects:
        if obj.type == "MESH":
            obj.hide_render = obj not in selected
        elif obj.type == "LIGHT":
            obj.hide_render = True
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 16
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    clay = bpy.data.materials.new("Stage review clay")
    clay.diffuse_color = (0.62, 0.62, 0.62, 1.0)
    clay.use_nodes = True
    clay.node_tree.nodes.clear()
    bsdf = clay.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    output = clay.node_tree.nodes.new("ShaderNodeOutputMaterial")
    clay.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    bsdf.inputs["Base Color"].default_value = (0.62, 0.62, 0.62, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bpy.context.view_layer.material_override = clay

    world = bpy.data.worlds.new("Stage review ambient")
    world.use_nodes = True
    world.node_tree.nodes.clear()
    background = world.node_tree.nodes.new("ShaderNodeBackground")
    world_output = world.node_tree.nodes.new("ShaderNodeOutputWorld")
    world.node_tree.links.new(background.outputs["Background"], world_output.inputs["Surface"])
    background.inputs["Color"].default_value = (0.45, 0.45, 0.45, 1.0)
    background.inputs["Strength"].default_value = 0.8
    scene.world = world

    camera_data = bpy.data.cameras.new("Stage review orthographic camera")
    camera = bpy.data.objects.new("Stage review orthographic camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = span * 1.55
    camera_data.lens = 50

    light_data = bpy.data.lights.new("Stage review key", type="AREA")
    light = bpy.data.objects.new("Stage review key", light_data)
    scene.collection.objects.link(light)
    light_data.energy = 400 * span * span
    light_data.shape = "DISK"
    light_data.size = span * 2.0

    outputs = {}
    for name, direction in VIEWS.items():
        camera.location = center + Vector(direction).normalized() * span * 3.0
        camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
        light.location = center + Vector(direction).normalized() * span * 2.0 + Vector((0.0, 0.0, span))
        light.rotation_euler = (center - light.location).to_track_quat("-Z", "Y").to_euler()
        path = stage_dir / f"{name}.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Render missing or empty: {path}")
        outputs[name] = path.name
    return outputs


def main():
    args = arguments()
    source = Path(bpy.data.filepath)
    if not source.is_file():
        raise ValueError("Load a saved .blend before invoking stage_review.py")
    stage_dir = Path(args.output).expanduser().resolve() / args.stage
    if stage_dir.exists():
        raise FileExistsError(f"Checkpoint already exists: {stage_dir}")

    objs = selected_meshes(args.object)
    center, span, low, high = world_bounds(objs)
    object_report = [
        {"name": obj.name, "vertices": len(obj.data.vertices), "faces": len(obj.data.polygons)}
        for obj in objs
    ]

    stage_dir.mkdir(parents=True)
    checkpoint = stage_dir / f"{args.stage}.blend"
    # Save before adding the temporary camera or changing render settings.
    bpy.ops.wm.save_as_mainfile(filepath=str(checkpoint), copy=True)
    if not checkpoint.is_file():
        raise RuntimeError(f"Checkpoint was not created: {checkpoint}")

    views = render_views(stage_dir, objs, center, span, args.resolution)
    report = {
        "blender_version": bpy.app.version_string,
        "source": str(source),
        "stage": args.stage,
        "checkpoint": checkpoint.name,
        "objects": object_report,
        "bounds_min": list(low),
        "bounds_max": list(high),
        "views": views,
        "convention": "Z up; front of subject faces -Y",
        "assessment": "Visual form and anatomy require human or agent image review; this report gives no quality score.",
    }
    (stage_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("STAGE_REVIEW_OK " + json.dumps({"stage_dir": str(stage_dir), "views": views}))


if __name__ == "__main__":
    main()
