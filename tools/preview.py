"""Orthographic SVG preview derived from the exported mesh, not a photograph."""

from html import escape

from tools.geometry import cross, dot, subtract


def render_svg(triangles, color, title):
    def project(p):
        x, y, z = p
        return (x - y, (x + y) * 0.42 - z)

    projected = [project(p) for triangle in triangles for p in triangle]
    low = [min(p[i] for p in projected) for i in range(2)]
    high = [max(p[i] for p in projected) for i in range(2)]
    scale = min(540 / (high[0] - low[0]), 310 / (high[1] - low[1]))
    offsets = [(700 - (high[0] - low[0]) * scale) / 2, (460 - (high[1] - low[1]) * scale) / 2]
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    visible = []
    for triangle in triangles:
        normal = cross(subtract(triangle[1], triangle[0]), subtract(triangle[2], triangle[0]))
        if dot(normal, (1, 1, 0.84)) <= 0:
            continue
        shade = 1 if normal[2] > 0 else (0.72 if normal[0] > 0 else 0.86)
        fill = "#" + "".join(f"{round(c * shade):02x}" for c in rgb)
        points = " ".join(
            f"{(project(p)[0] - low[0]) * scale + offsets[0]:.3f},"
            f"{(project(p)[1] - low[1]) * scale + offsets[1]:.3f}"
            for p in triangle
        )
        depth = sum(p[0] + p[1] + p[2] * 0.84 for p in triangle)
        visible.append((depth, f'<polygon points="{points}" fill="{fill}" stroke="{fill}" stroke-width="0.5"/>'))
    polygons = "".join(polygon for _, polygon in sorted(visible))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 460" role="img" aria-labelledby="title">'
        f'<title id="title">{escape(title)}: generated geometry preview, not a print photo</title>'
        f'{polygons}</svg>\n'
    )
