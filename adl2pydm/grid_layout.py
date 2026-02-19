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
        x_coords.update([geom.x, geom.x + geom.width])
        y_coords.update([geom.y, geom.y + geom.height])

    x_sorted = sorted(x_coords)
    y_sorted = sorted(y_coords)
    x_index = {x: i for i, x in enumerate(x_sorted)}
    y_index = {y: i for i, y in enumerate(y_sorted)}

    placements = []
    for ref, geom in widgets_with_geometry:
        col = x_index[geom.x]
        row = y_index[geom.y]
        placements.append((
            ref,
            GridPlacement(
                row,
                col,
                max(1, y_index[geom.y + geom.height] - row),
                max(1, x_index[geom.x + geom.width] - col),
            ),
        ))

    col_stretches = [x_sorted[i + 1] - x_sorted[i] for i in range(len(x_sorted) - 1)]
    row_stretches = [y_sorted[i + 1] - y_sorted[i] for i in range(len(y_sorted) - 1)]

    return {
        "placements": placements,
        "col_stretches": col_stretches,
        "row_stretches": row_stretches,
    }
