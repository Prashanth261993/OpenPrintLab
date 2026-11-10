"""Original bounded CAD designs, promoted from T-05 concepts. CC-BY-4.0."""


def validate_relations(identifier, p):
    if p["height"] - p["base"] < 2:
        raise ValueError("At least 2 mm must remain above the base")
    if p["radius"] > min(p["length"], p["width"]) / 4:
        raise ValueError("Radius must not exceed one quarter of the smaller horizontal dimension")
    if p["radius"] and p["radius"] < 1:
        raise ValueError("Radius must be zero or at least 1 mm")
    if identifier == "rounded-organizer":
        if p["radius"] and p["radius"] < p["wall"] + 0.5:
            raise ValueError("Organizer radius must be zero or at least wall + 0.5 mm")
        gap = (p["length"] - (p["compartments"] + 1) * p["wall"]) / p["compartments"]
        if gap < max(6, p["radius"] - p["wall"] + 0.5) or p["width"] - 2 * p["wall"] < 8:
            raise ValueError("Compartments must fit the walls and rounded-corner clearance")
    elif identifier == "rounded-pen-rest":
        if (p["width"] - (p["channels"] + 1) * p["wall"]) / p["channels"] < 6:
            raise ValueError("Each pen channel must be at least 6 mm wide")
    elif identifier == "paper-card-stand":
        if (p["width"] - p["slot_width"]) / 2 < 3 or p["length"] - 2 * p["end_margin"] < 20:
            raise ValueError("Slot must leave 3 mm side walls and at least 20 mm usable length")
    else:
        raise ValueError(f"Unknown CAD design: {identifier}")


def make_shape(identifier, p, cq):
    validate_relations(identifier, p)
    length, width, height = (p[key] for key in ("length", "width", "height"))

    def rounded_box(x, y, z, radius):
        body = cq.Workplane("XY").box(x, y, z, centered=(False, False, False))
        return body.edges("|Z").fillet(radius) if radius else body

    body = rounded_box(length, width, height, p["radius"])
    if identifier == "rounded-organizer":
        wall = p["wall"]
        inner = rounded_box(length - 2 * wall, width - 2 * wall, height, p["radius"] - wall if p["radius"] else 0)
        body = body.cut(inner.translate((wall, wall, p["base"])), clean=False)
        count = int(p["compartments"])
        gap = (length - (count + 1) * wall) / count
        for i in range(1, count):
            x = wall + i * gap + (i - 1) * wall
            divider = cq.Workplane("XY").box(wall, width, height - p["base"], centered=(False, False, False))
            body = body.union(divider.translate((x, 0, p["base"])), clean=False)
    elif identifier == "rounded-pen-rest":
        count, wall = int(p["channels"]), p["wall"]
        gap = (width - (count + 1) * wall) / count
        for i in range(count):
            groove = cq.Workplane("XY").box(length + 2, gap, height, centered=(False, False, False))
            body = body.cut(groove.translate((-1, wall + i * (gap + wall), p["base"])), clean=False)
    else:
        slot = cq.Workplane("XY").box(length - 2 * p["end_margin"], p["slot_width"], height, centered=(False, False, False))
        body = body.cut(slot.translate((p["end_margin"], (width - p["slot_width"]) / 2, p["base"])), clean=False)
    return body.val()
