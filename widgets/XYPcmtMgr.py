from ..defaults import DEFAULT_FONT
from ..bases import PcmtMgr
from operators import itemgetter as _ig
_firstgetter = _ig(0)
class XYPcmtMgr(PcmtMgr):
    def __init__(self,bg=(0,0,0,0),w=500,h=500):
        self.width = w
        self.height = h
        self._childs = []
    def add(self,child,pos):
        self._childs.append((child,pos))
    def get_surface(self):
        surf = self.blank()
        for widg,pos in self._childs:
            widg.place_at(pos,surf)
        return surf
    @property
    def childs(self):
        return tuple(map(_firstgetter,self._childs))
