"""Depth-buffered previews of actual mesh triangles. MIT; no imaging dependency."""

import base64
from html import escape
import math
import struct
import zlib

from tools.geometry import cross, dot, subtract


def rasterize_faces(faces, width, height):
    pixels = bytearray(width * height * 4)
    depths = [-math.inf] * (width * height)
    for vertices, color in faces:
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = vertices
        denominator = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(denominator) < 1e-12:
            continue
        left, right = max(0, math.floor(min(ax, bx, cx))), min(width - 1, math.ceil(max(ax, bx, cx)))
        top, bottom = max(0, math.floor(min(ay, by, cy))), min(height - 1, math.ceil(max(ay, by, cy)))
        rgba = bytes((*color, 255))
        for y in range(top, bottom + 1):
            py = y + 0.5
            for x in range(left, right + 1):
                px = x + 0.5
                a = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / denominator
                b = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / denominator
                c = 1 - a - b
                if min(a, b, c) < -1e-9:
                    continue
                depth = a * az + b * bz + c * cz
                index = y * width + x
                if depth > depths[index]:
                    depths[index] = depth
                    pixels[index * 4:index * 4 + 4] = rgba
    return bytes(pixels)


def _png(pixels, width, height):
    def chunk(name, data):
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)
    rows = b"".join(b"\0" + pixels[y * width * 4:(y + 1) * width * 4] for y in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows))
        + chunk(b"IEND", b"")
    )


def render_svg(triangles, color, title):
    width, height = 700, 460
    def project(p):
        return p[0] - p[1], (p[0] + p[1]) * 0.42 - p[2], p[0] + p[1] + p[2] * 0.84
    projected = [project(p) for face in triangles for p in face]
    low = [min(p[i] for p in projected) for i in range(2)]
    high = [max(p[i] for p in projected) for i in range(2)]
    scale = min(540 / (high[0] - low[0]), 310 / (high[1] - low[1]))
    offsets = [(width - (high[0] - low[0]) * scale) / 2, (height - (high[1] - low[1]) * scale) / 2]
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    faces = []
    for triangle in triangles:
        normal = cross(subtract(triangle[1], triangle[0]), subtract(triangle[2], triangle[0]))
        if dot(normal, (1, 1, 0.84)) <= 0:
            continue
        length = math.sqrt(dot(normal, normal))
        shade = 0.55 + 0.45 * max(0, dot(tuple(n / length for n in normal), (0.25, -0.4, 0.88)))
        vertices = []
        for point in triangle:
            x, y, depth = project(point)
            vertices.append(((x - low[0]) * scale + offsets[0], (y - low[1]) * scale + offsets[1], depth))
        faces.append((vertices, tuple(round(channel * shade) for channel in rgb)))
    image = base64.b64encode(_png(rasterize_faces(faces, width, height), width, height)).decode()
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 460" role="img" aria-labelledby="title">'
        f'<title id="title">{escape(title)}: depth-buffered exported geometry, not a print photo</title>'
        f'<image width="700" height="460" href="data:image/png;base64,{image}"/></svg>\n'
    )
