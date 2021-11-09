from ..bases import PcmtMgr
from operator import itemgetter as _ig
_firstgetter = _ig(0)
class XYPcmtMgr(PcmtMgr):
    def __init__(self,bg=(0,0,0,0),w=500,h=500):
        self.width = w
        self.height = h
        self._childs = []
    def add(self,child,pos):
        self._childs.append((child,pos))
    def enumerate_childs(self):
        for ch,po in self._childs:
            yield ch,(po[1],po[0])
    @property
    def childs(self):
        return tuple(map(_firstgetter,self._childs))
