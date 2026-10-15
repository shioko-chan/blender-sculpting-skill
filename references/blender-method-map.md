# Translating character and stylized sculpt methods into Blender

This is an original adaptation of common character sculpting principles, informed by the sources listed in [sources-and-license.md](sources-and-license.md). The entries are workflow correspondences, not claims that the two applications implement identical tools.

| Source method or intention | Practical Blender choice | Boundary to check |
| --- | --- | --- |
| Rough subtools and DynaMesh mass union | Separate Objects/Collections for exploration; duplicate a checkpoint, join selected meshes and use Sculpt Mode Voxel Remesh only when a continuous surface is needed. | Voxel remesh changes topology and can close gaps or soften thin forms; preserve the earlier objects. |
| ZRemesher after a sculpt | Manual retopology, or QuadriFlow as a starting mesh. | Automatic topology rarely settles facial loops or animation deformation requirements alone. |
| Subdivision levels / HD detail | Multiresolution modifier on a clean, stable base; inspect low and high levels separately. | Establish proportions first. Do not remesh the sculpt afterward expecting the same subdivision history. |
| Polygroups and isolated sculpt regions | Blender Face Sets, masks, and separate Objects. | Face Sets organize work but are not independent geometry. |
| Sculpt layers or morph targets | Duplicate stage `.blend` files; use Shape Keys for expressions on unchanged topology. | Shape Keys require matching vertex order and count. Voxel remesh, Dyntopo, and retopology break that relationship. |
| Curve-based hair clumps, horns, and straps | Curves with bevel for paths; convert to mesh only when local sculpting is needed. Keep broad clumps separate during blockout. | Hair curves and strand grooming are separate workflows; tiny strands should wait until silhouette works. |
| Surface Noise, alpha pores, scale stamps | Blender displacement or texture-driven brush detail on a high-resolution, approved form. | Use appropriately licensed alphas and compare at delivery resolution. Avoid uniform noise everywhere. |

## Character and creature reasoning

Start with skull/rib cage/pelvis or equivalent skeletal anchors, then connect major volumes through visible landmarks and joints. For faces, check the relationship of cranium, orbital sockets, cheek masses, jaw angle, muzzle or mouth mound, and neck before carving feature lines. A wrinkle, scale, or pore should have a regional cause or material logic. Test creature designs for stable stance and believable articulation, even when anatomy is invented. Use multiple species references when useful, recording which structure each reference informs.

## Stylized reasoning

Begin from plausible structure, then name a small number of exaggerations: for example, head-to-body ratio, hand size, jaw taper, or eye spacing. Recheck neighboring masses after each change so the whole design stays coherent. Design both positive masses and negative spaces. Favor a few deliberate curves and plane changes over evenly spaced details. Check silhouette at the target display size before refining eyes, hair, costume seams, or surface pattern.

The user may choose a different art direction. These checks identify contradictions to inspect, not universal proportions or a single preferred style.
