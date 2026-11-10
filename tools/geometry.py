"""Deterministic orthogonal solid meshing and bounded checks. MIT license."""

from collections import Counter, defaultdict, deque
from itertools import product
import math
import struct


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mesh_union(boxes):
    """Mesh exposed grid-cell faces; a shared global grid avoids T-junctions."""
    if not boxes or len(boxes) > 32:
        raise ValueError("Expected 1 to 32 boxes")
    for box in boxes:
        if len(box) != 6 or not all(math.isfinite(v) for v in box):
            raise ValueError("Boxes must have six finite coordinates")
        if any(box[i] >= box[i + 3] for i in range(3)):
            raise ValueError("Boxes must have positive dimensions")
    axes = [sorted({round(b[i], 6) for b in boxes} | {round(b[i + 3], 6) for b in boxes}) for i in range(3)]
    if any(len(axis) > 40 for axis in axes):
        raise ValueError("Grid too complex")
    cells = set()
    for cell in product(*(range(len(a) - 1) for a in axes)):
        middle = [(axes[i][cell[i]] + axes[i][cell[i] + 1]) / 2 for i in range(3)]
        if any(all(b[i] <= middle[i] <= b[i + 3] for i in range(3)) for b in boxes):
            cells.add(cell)
    triangles = []
    for cell in sorted(cells):
        low = [axes[i][cell[i]] for i in range(3)]
        high = [axes[i][cell[i] + 1] for i in range(3)]
        # Cyclic in-plane axes give +normal winding; reverse for negative faces.
        for axis in range(3):
            u, v = (axis + 1) % 3, (axis + 2) % 3
            for sign in (-1, 1):
                neighbor = list(cell)
                neighbor[axis] += sign
                if tuple(neighbor) in cells:
                    continue
                corners = []
                for a, b in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    point = list(low)
                    point[axis] = low[axis] if sign == -1 else high[axis]
                    point[u], point[v] = (high[u] if a else low[u]), (high[v] if b else low[v])
                    corners.append(tuple(point))
                if sign == -1:
                    corners.reverse()
                triangles.extend([(corners[0], corners[1], corners[2]), (corners[0], corners[2], corners[3])])
    return triangles


def encode_stl(triangles):
    data = bytearray(b"OpenPrintLab | millimeters | CC BY 4.0".ljust(80, b"\0"))
    data.extend(struct.pack("<I", len(triangles)))
    for a, b, c in triangles:
        n = cross(subtract(b, a), subtract(c, a))
        norm = math.sqrt(dot(n, n))
        if norm <= 1e-10:
            raise ValueError("Degenerate triangle")
        data.extend(struct.pack("<12fH", *(v / norm for v in n), *a, *b, *c, 0))
    return bytes(data)


def decode_stl(data):
    if len(data) < 84:
        raise ValueError("Truncated binary STL")
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + 50 * count or count == 0:
        raise ValueError("Invalid STL length or triangle count")
    triangles = []
    for i in range(count):
        values = struct.unpack_from("<12fH", data, 84 + i * 50)
        triangles.append(tuple(tuple(values[j:j + 3]) for j in (3, 6, 9)))
    return triangles


def validate_mesh(triangles):
    """Check exported triangles, not a claim of slicer or physical validation."""
    if not triangles:
        raise ValueError("Empty mesh")
    edges = Counter()
    graph = defaultdict(set)
    faces = set()
    volume = 0.0
    vertices = set()
    for a, b, c in triangles:
        if not all(math.isfinite(v) for point in (a, b, c) for v in point):
            raise ValueError("Non-finite mesh coordinate")
        normal = cross(subtract(b, a), subtract(c, a))
        if dot(normal, normal) < 1e-12:
            raise ValueError("Degenerate triangle")
        face = tuple(sorted((a, b, c)))
        if face in faces:
            raise ValueError("Duplicate triangle")
        faces.add(face)
        volume += dot(a, cross(b, c)) / 6
        vertices.update((a, b, c))
        for start, end in ((a, b), (b, c), (c, a)):
            edges[start, end] += 1
            graph[start].add(end)
            graph[end].add(start)
    if any(count != 1 or edges[end, start] != 1 for (start, end), count in edges.items()):
        raise ValueError("Mesh is open, non-manifold at an edge, or inconsistently wound")
    seen = set()
    queue = deque([next(iter(vertices))])
    while queue:
        vertex = queue.popleft()
        if vertex not in seen:
            seen.add(vertex)
            queue.extend(graph[vertex] - seen)
    if len(seen) != len(vertices):
        raise ValueError("Mesh has disconnected components")
    if volume <= 0:
        raise ValueError("Mesh volume must be positive with outward winding")
    low = [min(v[i] for v in vertices) for i in range(3)]
    high = [max(v[i] for v in vertices) for i in range(3)]
    size = [round(high[i] - low[i], 4) for i in range(3)]
    if min(low) < -0.0001 or abs(low[2]) > 0.0001 or max(high) > 256:
        raise ValueError("Mesh must sit at Z=0 inside the P2S 256 mm build envelope")
    return {
        "dimensions_mm": size, "triangles": len(triangles), "volume_mm3": round(volume, 3),
        "closed_edges": True, "consistent_winding": True, "connected": True,
        "nondegenerate": True, "within_p2s_envelope": True,
    }
