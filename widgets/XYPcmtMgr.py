from ..bases import PcmtMgr
from operator import itemgetter as _ig
_firstgetter = _ig(0)
class XYPcmtMgr(PcmtMgr):
    """\
An XY Coordinates based placement manager.

Constructor: XYPcmtMgr([width,[height,[background]]])
Signature: __init__(self,w=500,h=500,bg=(0,0,0,0))
background is the base color of the generated image.
width and height specifies the dimensions of the generated surface.
"""
    def __init__(self,w=500,h=500,bg=(0,0,0,0)):
        self.width = w
        self.height = h
        self.bg = bg
        self._childs = []
    def blank(self):
        """\
Overrides the default blank() implementation to add background color."""
        blnk = super().blank()
        blnk.fill(self.bg)
        return blnk
    def add(self,child,pos):
        self._childs.append((child,pos))
    def remove(self,child,noerror=False):
        """\
WARNING: Linear O(N) Complexity! Not fast!"""
        rmv = -1
        for i,(chl,p) in enumerate(self._childs):
            if chl==child:
                rmv = i
                break
        if (rmv == -1) and (not noerror):
            raise IndexError(
f"Widget not found: removing {child}(of class {type(child).__name__})")
        if (rmv != -1):
            del self._childs[rmv]
    def enumerate_childs(self):
        for ch,po in self._childs:
            yield (ch,po)
    @property
    def childs(self):
        return tuple(map(_firstgetter,self._childs))
