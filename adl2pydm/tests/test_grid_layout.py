"""Unit tests for grid_layout module."""

from ..adl_parser import Geometry
from ..grid_layout import GridPlacement, compute_grid_placement


def test_single_widget_fills_container():
    widgets = [("w1", Geometry(0, 0, 100, 100))]
    result = compute_grid_placement(widgets, 100, 100)
    assert len(result["placements"]) == 1
    ref, gp = result["placements"][0]
    assert ref == "w1"
    assert gp == GridPlacement(row=0, col=0, rowspan=1, colspan=1)
    assert result["col_stretches"] == [100]
    assert result["row_stretches"] == [100]


def test_two_side_by_side():
    widgets = [
        ("w1", Geometry(0, 0, 50, 100)),
        ("w2", Geometry(50, 0, 50, 100)),
    ]
    result = compute_grid_placement(widgets, 100, 100)
    assert len(result["placements"]) == 2
    assert result["col_stretches"] == [50, 50]
    assert result["row_stretches"] == [100]
    _, gp1 = result["placements"][0]
    _, gp2 = result["placements"][1]
    assert gp1 == GridPlacement(0, 0, 1, 1)
    assert gp2 == GridPlacement(0, 1, 1, 1)


def test_widget_with_margins():
    """Widget inset from container edges creates margin columns/rows."""
    widgets = [("w1", Geometry(10, 20, 80, 60))]
    result = compute_grid_placement(widgets, 100, 100)
    # x: [0, 10, 90, 100] -> 3 cols, stretches [10, 80, 10]
    # y: [0, 20, 80, 100] -> 3 rows, stretches [20, 60, 20]
    assert result["col_stretches"] == [10, 80, 10]
    assert result["row_stretches"] == [20, 60, 20]
    _, gp = result["placements"][0]
    assert gp == GridPlacement(row=1, col=1, rowspan=1, colspan=1)


def test_overlapping_widgets():
    widgets = [
        ("bg", Geometry(0, 0, 200, 200)),
        ("fg", Geometry(50, 50, 100, 100)),
    ]
    result = compute_grid_placement(widgets, 200, 200)
    # x: [0, 50, 150, 200] -> 3 cols
    # y: [0, 50, 150, 200] -> 3 rows
    assert result["col_stretches"] == [50, 100, 50]
    assert result["row_stretches"] == [50, 100, 50]
    _, bg_gp = result["placements"][0]
    assert bg_gp == GridPlacement(row=0, col=0, rowspan=3, colspan=3)
    _, fg_gp = result["placements"][1]
    assert fg_gp == GridPlacement(row=1, col=1, rowspan=1, colspan=1)


def test_grid_2x2():
    widgets = [
        ("tl", Geometry(0, 0, 50, 50)),
        ("tr", Geometry(50, 0, 50, 50)),
        ("bl", Geometry(0, 50, 50, 50)),
        ("br", Geometry(50, 50, 50, 50)),
    ]
    result = compute_grid_placement(widgets, 100, 100)
    assert result["col_stretches"] == [50, 50]
    assert result["row_stretches"] == [50, 50]
    refs = {ref: gp for ref, gp in result["placements"]}
    assert refs["tl"] == GridPlacement(0, 0, 1, 1)
    assert refs["tr"] == GridPlacement(0, 1, 1, 1)
    assert refs["bl"] == GridPlacement(1, 0, 1, 1)
    assert refs["br"] == GridPlacement(1, 1, 1, 1)


def test_spanning_widget():
    """Widget spanning the full width of the container."""
    widgets = [
        ("top_left", Geometry(0, 0, 50, 50)),
        ("top_right", Geometry(50, 0, 50, 50)),
        ("bottom", Geometry(0, 50, 100, 50)),
    ]
    result = compute_grid_placement(widgets, 100, 100)
    refs = {ref: gp for ref, gp in result["placements"]}
    assert refs["bottom"] == GridPlacement(row=1, col=0, rowspan=1, colspan=2)


def test_zero_size_widget():
    """Zero-width/height widgets (MEDM lines) get span clamped to 1."""
    widgets = [
        ("hline", Geometry(10, 50, 80, 0)),  # horizontal line, height=0
        ("vline", Geometry(50, 10, 0, 80)),  # vertical line, width=0
    ]
    result = compute_grid_placement(widgets, 100, 100)
    refs = {ref: gp for ref, gp in result["placements"]}
    assert refs["hline"].rowspan >= 1
    assert refs["hline"].colspan >= 1
    assert refs["vline"].rowspan >= 1
    assert refs["vline"].colspan >= 1
