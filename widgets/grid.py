"""A 2D grid."""
from ..bases import Widget
from pygame.draw import rect
class _Wrap:
    """Wrapper to handle list/dict indexes."""
    def __init__(self,dat):
        self.NULL = (dat is None)
        self.d = dat
    def __getitem__(self,x):
        if self.NULL:
            return None
        if (self.d.__class__ is dict)and(x not in self.d):
            return None
        return self.d[x]
    def __setitem__(self,x,t):
        self.d[x] = t
    def inrange(self,x):
        if (self.d.__class__ is dict):
            return True
        return x in range(len(self.d))
class _GridData:
    """Infinite 2D array."""
    def __init__(self,w,h):
        if w==None:
            self.data = {}
        else:
            self.data = [({} if h is None else [None for j in range(h)])
                         for i in range(w)]
        self.w = w
        self.h = h
    def __getitem__(self,x):
        if _Wrap(self.data)[x] is None:
            self.data[x] = ({} if self.h is None else [None for j in range(h)])
        return _Wrap(_Wrap(self.data)[x])
    def inrange(self,x):
        return _Wrap(self.data).inrange(x)
class Grid(Widget):
    """2D grid.
Arguments:
w: width of widget
h: height of widget
gridw: width of a single cell.
gridh: height of a single cell.
wgrids: width of the grid(unit:cells). If None, is infinite in width.
hgrids: height of the grid(unit:cells). If None, is infinite in height.
NOTE: Making a grid infinite may degrade performance.

borderw: width of border(in pixels)(will cover cells)
bordercolor: color of border
"""
    def __init__(self,w,h,gridw,gridh,wgrids=None,hgrids=None,borderw=2,
                 bordercolor=(0,0,0)):
        self.width = w
        self.height = h
        self.data = _GridData(wgrids,hgrids)
        self.gw = gridw
        self.gh = gridh
        self.bw = borderw
        self.bc = bordercolor
    def get(self,x,y):
        return self.data[x][y]
    def set(self,x,y,v):
        self.data[x][y] = v
    def get_surface(self):
        blnk = self.blank()
        co = 0
        ro = 0
        #Performance optimizations
        gw = self.gw
        gh = self.gh
        wi = self.width
        he = self.height
        while True:
            da = self.data[co][ro]
            if da is not None:
                blnk.blit(da.get_surface(),(co*gw,ro*gh))
            co += 1
            if (co*gw)>wi:#out of screen
                co = 0
                ro += 1
                if (ro*gh)>he:#out of screen:done
                    break
        #grid lines
        bw = self.bw
        if bw > 0:
            bc = self.bc
            hbw = bw//2
            co = 1#CO lines
            while (co*gw)<wi:
                rec = (co*gw-hbw,0,bw,he)
                rect(blnk,bc,rec)
                co += 1
            ro = 1#RO lines
            while (ro*gh)<he:
                rec = (0,ro*gh-hbw,wi,bw)
                rect(blnk,bc,rec)
                ro += 1
        return blnk
    def handle_event(self,evt):
        if hasattr(evt,"pos"):
            pos = evt.pos
            x = pos[0]//self.gw
            y = pos[1]//self.gh
            if (not self.data.inrange(x))or(not self.data[x].inrange(y))or(
                self.data[x][y] is None):
                return False
            return self.data[x][y].handle_event(evt)
        return False
