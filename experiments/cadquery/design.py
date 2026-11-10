"""Original experimental tray design. SPDX-License-Identifier: CC-BY-4.0."""

from dataclasses import dataclass
import math

import cadquery as cq


@dataclass(frozen=True)
class TrayParameters:
    length: float = 96
    width: float = 64
    height: float = 16
    wall: float = 2.4
    base: float = 2
    radius: float = 6


def validate(p):
    limits = {
        "length": (60, 160), "width": (40, 120), "height": (10, 30),
        "wall": (2, 3), "base": (1.6, 3), "radius": (0, 30),
    }
    for name, (low, high) in limits.items():
        value = getattr(p, name)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite number in mm")
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"{name} must be between {low} and {high} mm")
    if p.height - p.base < 4:
        raise ValueError("At least 4 mm must remain above the base")
    if p.radius != 0 and not p.wall + 0.5 <= p.radius <= min(p.length, p.width) / 4:
        raise ValueError("Radius must be zero or between wall + 0.5 and min(length,width)/4")


def make_tray(p):
    validate(p)
    outer = cq.Workplane("XY").box(p.length, p.width, p.height, centered=(False, False, False))
    inner = cq.Workplane("XY").box(p.length - 2 * p.wall, p.width - 2 * p.wall, p.height, centered=(False, False, False))
    if p.radius:
        outer = outer.edges("|Z").fillet(p.radius)
        inner = inner.edges("|Z").fillet(p.radius - p.wall)
    inner = inner.translate((p.wall, p.wall, p.base))
    return outer.cut(inner, clean=False).val()


def analytic_volume(p):
    validate(p)
    outer_area = p.length * p.width
    inner_area = (p.length - 2 * p.wall) * (p.width - 2 * p.wall)
    if p.radius:
        outer_area -= (4 - math.pi) * p.radius ** 2
        inner_area -= (4 - math.pi) * (p.radius - p.wall) ** 2
    return outer_area * p.height - inner_area * (p.height - p.base)
