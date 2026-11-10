"""Original parametric design source. SPDX-License-Identifier: CC-BY-4.0."""

import math


PARAMETERS = {
    "tray": {
        "length": (30, 200), "width": (24, 200), "height": (6, 50),
        "wall": (1.6, 5), "base": (1.2, 5), "dividers": (0, 4),
    },
    "rest": {
        "length": (30, 160), "width": (20, 120), "height": (4, 20),
        "wall": (1.6, 5), "base": (1.2, 5), "channels": (1, 5),
    },
    "steps": {
        "length": (16, 120), "width": (12, 100), "height": (4, 50),
        "steps": (2, 8),
    },
}
COUNTS = {"dividers", "channels", "steps"}


def validate_parameters(recipe, parameters):
    if recipe not in PARAMETERS:
        raise ValueError(f"Unknown recipe: {recipe}")
    rules = PARAMETERS[recipe]
    if set(parameters) != set(rules):
        raise ValueError(f"Expected exactly these parameters: {', '.join(rules)}")
    for name, value in parameters.items():
        low, high = rules[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number in mm (counts are unitless)")
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"{name} must be between {low} and {high}")
        if name in COUNTS and int(value) != value:
            raise ValueError(f"{name} must be a whole number")
    length, width, height = (parameters[k] for k in ("length", "width", "height"))
    if recipe == "steps":
        if length / parameters["steps"] < 4 or height / parameters["steps"] < 1:
            raise ValueError("Each tread must be >=4 mm and each rise >=1 mm")
    else:
        wall, base = parameters["wall"], parameters["base"]
        if height - base < 2:
            raise ValueError("Height must leave at least 2 mm above the base")
        if recipe == "tray":
            count = int(parameters["dividers"])
            if (length - (count + 2) * wall) / (count + 1) < 6 or width - 2 * wall < 6:
                raise ValueError("Each compartment must be at least 6 mm wide")
        elif (width - (parameters["channels"] + 1) * wall) / parameters["channels"] < 6:
            raise ValueError("Each channel must be at least 6 mm wide")


def boxes(recipe, parameters):
    """Return a union of axis-aligned boxes as (x0,y0,z0,x1,y1,z1), in mm."""
    validate_parameters(recipe, parameters)
    p = parameters
    length, width, height = (p[k] for k in ("length", "width", "height"))
    if recipe == "steps":
        count = int(p["steps"])
        return [
            (i * length / count, 0, 0, (i + 1) * length / count, width, (i + 1) * height / count)
            for i in range(count)
        ]
    wall, base = p["wall"], p["base"]
    result = [(0, 0, 0, length, width, base)]
    if recipe == "tray":
        result += [(0, 0, base, length, wall, height), (0, width - wall, base, length, width, height)]
        count = int(p["dividers"])
        gap = (length - (count + 2) * wall) / (count + 1)
        result += [
            (i * (gap + wall), wall, base, i * (gap + wall) + wall, width - wall, height)
            for i in range(count + 2)
        ]
    else:
        count = int(p["channels"])
        gap = (width - (count + 1) * wall) / count
        result += [
            (0, i * (gap + wall), base, length, i * (gap + wall) + wall, height)
            for i in range(count + 1)
        ]
    return result
