"""Custom widgets for adl2pydm-generated .ui files."""

import logging
import math

from pydm.widgets.frame import PyDMFrame
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class ScalableFrame(PyDMFrame):
    """
    PyDMFrame that scales all descendants proportionally on resize,
    mimicking MEDM's scaling behavior.
    """

    def __init__(self, parent=None, init_channel=None):
        super().__init__(parent=parent, init_channel=init_channel)
        self._geometry_captured = False
        self._original_size = None
        self._originals = {}

    def showEvent(self, event):
        super().showEvent(event)
        if not self._geometry_captured:
            QTimer.singleShot(0, self._capture_geometry)

    def _capture_geometry(self):
        if self._geometry_captured:
            return
        self._original_size = (self.width(), self.height())
        for child in self._iter_descendants():
            geom = child.geometry()
            font = child.font()
            self._originals[id(child)] = {
                "ref": child,
                "x": geom.x(),
                "y": geom.y(),
                "w": geom.width(),
                "h": geom.height(),
                "pt": font.pointSizeF() if font.pointSizeF() > 0 else None,
            }
        self._geometry_captured = True

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self._geometry_captured or not self._original_size:
            return
        ow, oh = self._original_size
        if ow <= 0 or oh <= 0:
            return
        sx = self.width() / ow
        sy = self.height() / oh

        for orig in self._originals.values():
            child = orig["ref"]
            child.setGeometry(
                int(orig["x"] * sx),
                int(orig["y"] * sy),
                max(1, int(orig["w"] * sx)),
                max(1, int(orig["h"] * sy)),
            )
            if orig["pt"] is not None:
                font = child.font()
                font.setPointSizeF(max(4.0, orig["pt"] * math.sqrt(sx * sy)))
                child.setFont(font)

    def _iter_descendants(self):
        """Yield MEDM-placed widgets only.

        Recurse into PyDMFrame (MEDM composite containers) but not into
        other widget types whose children are internal Qt/PyDM controls
        (e.g. plot axes, scrollbar parts, scale labels).
        """
        stack = list(self.children())
        while stack:
            child = stack.pop()
            if isinstance(child, QWidget):
                yield child
                if isinstance(child, PyDMFrame):
                    stack.extend(child.children())
