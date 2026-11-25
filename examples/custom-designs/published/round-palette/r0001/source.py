"""Original round bead palette; CC BY 4.0 OpenPrintLab contributors.

Self-contained geometry, one solid and no imported model assets.
Run only after reviewing this file, the brief and local tool permissions.
"""

import math

import cadquery as cq

from tools.designs import run_design


def make_shape(p):
    if set(p) != {"diameter", "height", "base", "well_diameter", "wells"}:
        raise ValueError("Unexpected palette parameters")
    diameter, height, base, well = (p[k] for k in ("diameter", "height", "base", "well_diameter"))
    count = p["wells"]
    if not (50 <= diameter <= 100 and 5 <= height <= 15 and 2 <= base <= height - 2
            and 8 <= well <= 18 and count == int(count) and 3 <= count <= 8):
        raise ValueError("Palette parameter bounds violated")
    radius = diameter / 2 - well / 2 - 4
    if 2 * radius * math.sin(math.pi / count) - well < 2:
        raise ValueError("Wells must leave at least 2 mm between openings")
    body = cq.Workplane("XY").circle(diameter / 2).extrude(height)
    for i in range(int(count)):
        angle = 2 * math.pi * i / count
        cutter = (cq.Workplane("XY").center(radius * math.cos(angle), radius * math.sin(angle))
                  .circle(well / 2).extrude(height).translate((0, 0, base)))
        body = body.cut(cutter)
    return body.translate((diameter / 2, diameter / 2, 0)).val()


if __name__ == "__main__":
    run_design(__file__, make_shape)
