"""Geometry-derived orthographic overview drawings, not fabrication certification. MIT."""

import base64
import hashlib
import json

from tools.catalog import source_hash
from tools.designs import _safe_path
from tools.diagnostics import inspect_file
from tools.geometry import cross, decode_stl, subtract
from tools.mesh_preview import _png, rasterize_faces


def draw_stl(source, destination):
    source, destination = _safe_path(source), _safe_path(destination)
    if destination.exists():
        raise FileExistsError("Drawing directory exists; choose a new output")
    screening = inspect_file(source, mode="assembly")
    if screening["has_errors"]:
        raise ValueError("Mesh has diagnostic errors; resolve them before drawing")
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != screening["stl_sha256"]:
        raise ValueError("Source changed during inspection")
    triangles = decode_stl(data)
    views, payloads = {}, {}
    for name, axes, direction in (("top", (0, 1, 2), 1), ("front", (0, 2, 1), -1),
                                   ("right", (1, 2, 0), 1)):
        u, v, d = axes
        pts = [point for face in triangles for point in face]
        low = [min(p[k] for p in pts) for k in (u, v)]
        high = [max(p[k] for p in pts) for k in (u, v)]
        dimensions = [high[k] - low[k] for k in (0, 1)]
        if min(dimensions) <= 0:
            raise ValueError("Projection has zero extent")
        width, height = 700, 520
        scale = min(540 / dimensions[0], 320 / dimensions[1])
        left, top = (width - dimensions[0] * scale) / 2, 50 + (320 - dimensions[1] * scale) / 2
        right, bottom = left + dimensions[0] * scale, top + dimensions[1] * scale
        depth_low = min(p[d] * direction for p in pts)
        depth_range = max(p[d] * direction for p in pts) - depth_low
        faces = []
        for face in triangles:
            normal = cross(subtract(face[1], face[0]), subtract(face[2], face[0]))
            if normal[d] * direction <= 0:
                continue
            projected = [(left + (p[u] - low[0]) * scale, top + (high[1] - p[v]) * scale,
                          p[d] * direction) for p in face]
            depth = sum(p[2] for p in projected) / 3
            shade = 0.55 + 0.45 * (depth - depth_low) / max(depth_range, 1e-12)
            faces.append((projected, tuple(round(channel * shade) for channel in (73, 127, 112))))
        png = _png(rasterize_faces(faces, width, height), width, height)
        image = base64.b64encode(png).decode()
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/><image width="{width}" height="{height}" href="data:image/png;base64,{image}"/>
<g stroke="#333" fill="none"><path d="M {left} {bottom} V {bottom+35} H {right} V {bottom}"/>
<path d="M {right} {top} H {right+35} V {bottom} H {right}"/></g>
<g font-family="sans-serif" font-size="16" fill="#182c24">
<text x="25" y="28">{name.title()} - axes {"XYZ"[u]}/{"XYZ"[v]}</text>
<text data-dimension-mm="{dimensions[0]}" x="{(left+right)/2}" y="{bottom+58}" text-anchor="middle">{dimensions[0]:.3f} mm</text>
<text data-dimension-mm="{dimensions[1]}" x="{right+48}" y="{(top+bottom)/2}" text-anchor="middle" transform="rotate(-90 {right+48} {(top+bottom)/2})">{dimensions[1]:.3f} mm</text>
<text x="25" y="500" font-size="12">Overall mesh bounds only. Not to scale on paper. No feature tolerances or physical validation.</text>
</g></svg>"""
        payloads[f"{name}.svg"] = svg.encode()
        views[name] = {"axes": ["XYZ"[u], "XYZ"[v]], "dimensions_mm": dimensions,
                       "sha256": hashlib.sha256(payloads[f"{name}.svg"]).hexdigest()}
    report = {"source_stl_sha256": screening["stl_sha256"], "units": "mm", "views": views,
              "checker_source_sha256": source_hash("tools/drawings.py"),
              "renderer_source_sha256": source_hash("tools/mesh_preview.py"),
              "scope": "Orthographic triangulated geometry overview and overall extents only, not toleranced fabrication drawings.",
              "physical_print_tested": False, "slicer_checked": False}
    destination.mkdir(parents=True)
    for filename, payload in payloads.items():
        (destination / filename).write_bytes(payload)
    (destination / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
