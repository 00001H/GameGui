"""A 2D grid."""
from ..bases import Widget
from pygame.draw import rect
def arr2(wx,wy):
    return [[None for i in range(wy)] for i in range(wx)]
class Grid(Widget):
    """2D grid.
Arguments:
w: width of widget
h: height of widget
gridw: width of a single cell.
gridh: height of a single cell.
wgrids: width of the grid(unit:cells).
hgrids: height of the grid(unit:cells).
NOTE: Making a grid infinite may degrade performance.

borderw: width of border(in pixels)(will cover cells)
bordercolor: color of border
"""
    def __init__(self,w,h,gridw,gridh,wgrids=10,hgrids=10,borderw=2,
                 bordercolor=(0,0,0)):
        self.width = w
        self.height = h
        self.data = arr2(wgrids,hgrids)
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
            if (co*gw)>wi or co >= len(self.data):
                co = 0
                ro += 1
                if (ro*gh)>he or ro >= len(self.data[0]):
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
            if (x not in range(len(self.data)))or(y not in range(len(self.data[x])))or(
                self.data[x][y] is None):
                return False
            return self.data[x][y].handle_event(evt)
        return False
