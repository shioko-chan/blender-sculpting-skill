---
name: blender-form-sculpting
description: Plan, build, and review Blender character, creature, or stylized sculpts for proportion, anatomy, primary masses, silhouette, and readable forms across views. Use for sculpting or shape-modeling tasks, not merely Blender connection setup.
---

# Blender form sculpting

Use this skill when the requested result is a shaped 3D asset or an art critique. A Blender connection alone does not establish form quality. Work from the user's subject, references, style, pose, intended camera distance, and output needs. If references or target style are missing, state a practical assumption and keep it easy to revise.

## Capabilities and limits

- Blender is required to edit or render a `.blend`. The bundled `scripts/stage_review.py` needs Blender's bundled Python only; it makes a saved copy and multi-view clay renders from an existing scene. It does **not** sculpt, grade anatomy, or replace visual judgment.
- Prefer an existing live Blender session for actual brush strokes. Headless `bpy` is useful for object blockout, modifiers, file saves, measurements, and renders. Do not assume an interactive sculpt stroke operator works in background mode.
- Check `blender --version` and the relevant `bpy` API in that installation before using version-sensitive operators. This skill was smoke-tested on Blender 5.1.1. No sibling skill, ZBrush installation, or Scenario MCP is required.
- Do not promise a professional finished character from a procedural blockout. State which stages were actually made and visually reviewed.

## Working loop

1. **Define the read.** Record subject and age/species cues, pose, realism level, intended viewing distance, strongest silhouette, and one to three deliberate exaggerations. For likeness or realistic anatomy, use licensed reference images from front, side, and three-quarter views. Treat standard proportions as diagnostic starting points, not immutable measurements.
2. **Block primary masses.** Use separate editable objects for cranium, rib cage, pelvis, jaw/muzzle, limbs, horns, hair masses, or other defining volumes. Make the line of action, balance, overall width/height, negative spaces, and large plane changes readable with a plain clay material. Work at low resolution; avoid pores, tiny wrinkles, strands, and decorative cuts.
3. **Review before increasing resolution.** Save a named blockout checkpoint and inspect front, profile, three-quarter, and back renders at thumbnail size and full size. Write the most consequential defect, change the underlying mass or proportion, and repeat. Move on only when the subject and intended style read in silhouette from the relevant views.
4. **Build secondary forms.** Establish anatomical landmarks and how masses overlap: brow/orbit/cheek/jaw on heads; bony landmarks, joints, muscle groups, and load-bearing structure on bodies; skeletal logic and locomotion on creatures. Add features as volumes embedded in surrounding forms. Keep hair, clothing, horns, and props separately editable until their shapes settle. Check asymmetry on purpose, not by accident.
5. **Refine surface after the forms hold.** Choose voxel remesh for combining rough masses, then inspect lost edges and separate pieces. Choose Multiresolution only on a settled, suitable base mesh; topology-changing remesh or Dyntopo can invalidate later subdivision and shape keys. Use actual Blender Sculpt tools in a live session for plane and surface work. Keep microdetail subordinate to the design and camera distance.
6. **Review and deliver.** Save separate `blockout`, `primary`, `secondary`, and `final` checkpoints where those stages occur; never overwrite a previously accepted checkpoint. Render the same neutral framing from multiple views after each meaningful change. Compare to references and the brief, inspect images rather than relying on mesh counts, fix the largest remaining issue, then report remaining limitations.

Use [references/form-review.md](references/form-review.md) for view-specific critique and stage acceptance. For character, creature, or stylized workflows adapted from ZBrush methods, read [references/blender-method-map.md](references/blender-method-map.md). For provenance and license checks, see [references/sources-and-license.md](references/sources-and-license.md).

## Checkpoint and render helper

After saving the working `.blend`, run:

```bash
blender --background /absolute/path/character.blend --python-exit-code 1 \
  --python /absolute/path/blender-form-sculpting/scripts/stage_review.py -- \
  --stage blockout --output /absolute/path/reviews --resolution 512
```

The helper selects visible mesh objects by default. Pass `--object Head` to review one named mesh. It creates `reviews/blockout/blockout.blend`, `front.png`, `three_quarter.png`, `profile.png`, `back.png`, and `report.json`. It refuses an existing stage directory; use a new stage name for another pass. By convention the face points toward Blender `-Y`, with `Z` up; rotate the model or specify the appropriate orientation in the scene before using the helper. The images are clay previews, not surface-quality proof. Open all four images and record the concrete revisions.

## Install and use in Codex

Copy this whole directory to `~/.codex/skills/blender-form-sculpting/` or the target project's `.agents/skills/blender-form-sculpting/`, then start a new Codex session. Verify `blender --version`; the helper needs no Python packages beyond Blender. An optional Blender UI bridge or MCP connection helps with live brush work, but is not required to load the skill.

Example requests:

- “Use `$blender-form-sculpting` to block out a stylized fox bust in Blender. Save each stage and show front, profile, three-quarter, and back checks before adding fur detail.”
- “Use `$blender-form-sculpting` to critique this `.blend` for head proportion, jaw planes, silhouette, and consistency across views; give the three highest-impact fixes.”

For a finished asset, deliver the `.blend`, review images, checkpoint paths, a brief critique with accepted and unresolved points, and any render/export requested by the user.
