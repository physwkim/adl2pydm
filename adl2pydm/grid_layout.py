"""Compute QGridLayout placement from absolute widget geometries."""

from collections import namedtuple

GridPlacement = namedtuple("GridPlacement", "row col rowspan colspan")


def compute_grid_placement(widgets_with_geometry, container_width, container_height):
    """
    Compute QGridLayout row/col/span and stretch factors from widget geometries.

    Parameters
    ----------
    widgets_with_geometry : list of (ref, Geometry)
        Each entry is (arbitrary reference, Geometry(x, y, width, height)).
    container_width : int
        Width of the parent container.
    container_height : int
        Height of the parent container.

    Returns
    -------
    dict
        "placements": list of (ref, GridPlacement)
        "col_stretches": list of int
        "row_stretches": list of int
    """
    x_coords = {0, container_width}
    y_coords = {0, container_height}
    for _, geom in widgets_with_geometry:
        # Clamp coordinates to container bounds to prevent phantom widgets
        # (e.g. deleted MEDM composites at x=-2147483647) from creating
        # enormous stretch values that collapse the entire grid.
        x0 = max(0, min(geom.x, container_width))
        x1 = max(0, min(geom.x + geom.width, container_width))
        y0 = max(0, min(geom.y, container_height))
        y1 = max(0, min(geom.y + geom.height, container_height))
        x_coords.update([x0, x1])
        y_coords.update([y0, y1])

    x_sorted = sorted(x_coords)
    y_sorted = sorted(y_coords)
    x_index = {x: i for i, x in enumerate(x_sorted)}
    y_index = {y: i for i, y in enumerate(y_sorted)}

    placements = []
    for ref, geom in widgets_with_geometry:
        x0 = max(0, min(geom.x, container_width))
        y0 = max(0, min(geom.y, container_height))
        x1 = max(0, min(geom.x + geom.width, container_width))
        y1 = max(0, min(geom.y + geom.height, container_height))
        col = x_index[x0]
        row = y_index[y0]
        placements.append((
            ref,
            GridPlacement(
                row,
                col,
                max(1, y_index[y1] - row),
                max(1, x_index[x1] - col),
            ),
        ))

    col_stretches = [x_sorted[i + 1] - x_sorted[i] for i in range(len(x_sorted) - 1)]
    row_stretches = [y_sorted[i + 1] - y_sorted[i] for i in range(len(y_sorted) - 1)]

    return {
        "placements": placements,
        "col_stretches": col_stretches,
        "row_stretches": row_stretches,
    }
