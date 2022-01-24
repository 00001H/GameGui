from .text import Text,LEFT,CENTER,RIGHT,StyleChange
from .entry import Entry
from .linegraph import LineGraph
from .XYPcmtMgr import XYPcmtMgr
from .button import Button
from .grid import Grid
from ..bases import Widget
class NULL(Widget):
    def __init__(self):
        self.width = 1
        self.height = 1
    def get_surface(self):
        return self.blank()
NULLWIDGET = NULL()
del Widget,NULL
