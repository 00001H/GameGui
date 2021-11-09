"""The windows manager."""
from pygame import Rect
from pygame.display import set_mode
from ..bases import Transformation
from .._utils import LazyExpr,dictunion,focused_in
from ..events import _NodeWrapper
from ..widgets import XYPcmtMgr
DISPLAYWIN = None
__all__ = ["Window","config_window","getdisplaysurface","place"]
def _wrapped_of(w):
    w = _underlying(w)
    while isinstance(w,Transformation):
        w = _underlying(w.target)
    return w
def _underlying(x):
    if x is None:
        return None
    elif isinstance(x,_NodeWrapper):
        return x.n
    return x
class Window(XYPcmtMgr):
    """Represents a window.
Arguments:
dw: the surface to be bound to.If it is None,every draw option will be applied on the
display surface bound globally AT THE TIME OF THE DRAW CALL.

WARNING: Should never be a child of any other widget.Use XYPcmtMgr instead for
popup windows and sub-GUIs."""
    def __init__(self,dw=None):
        self._childs = []
        self._dw = dw
    def get_surface(self):
        raise NotImplementedError()
    @property
    def dw(self):
        return self._dw if (self._dw is not None) else DISPLAYWIN
    def update(self):
        """Updates the display surface(drawing the child components)."""
        self.RENDER_SURFACE = self.dw
        super().get_surface()#renders
        self.notify(self.childs)
    def notify(self,todo):
        for widg in todo:
            widg.on_update(_wrapped_of(focused_in(self)) is _wrapped_of(widg))
            self.notify(getattr(widg,"childs",[]))
    def fill(self,color,*a,**k):
        """Fills with a color.Extra options(like the rect) will be passed to the
Surface.fill() method."""
        self.dw.fill(color,*a,**k)
def config_window(width,height,flags=0):
    """Setups and returns the window with the specified dimensions and flags."""
    global DISPLAYWIN
    DISPLAYWIN = set_mode((width,height),flags)
    return DISPLAYWIN
def getdisplaysurface():
    """Returns the current display surface."""
    return DISPLAYWIN
def place(target,rendersurface,position,extra=None):
    """Blits the target to the rendersurface.
Default lazy expression values:(RS means rendersurface,T means target)
SW:width of RS
HSW:SW//2
SH:height of RS
HSH:SH//2
WW:width of T
HWW:WW//2
WH:height of T
HWH:WH//2

Position may be a string/LazyExpr,a 2-tuple(x,y),a pygame.Rect object or a 4-tuple(x,y,w,h).
Note:width and height are ignored."""
    rect = rendersurface.get_rect()
    if hasattr(target,"rect"):
        wrect = target.rect
    else:
        wrect = target.get_rect()
    sw,sh = rect.width,rect.height
    ww,wh = wrect.width,wrect.height
    if extra is None:
        extra = {}
    if isinstance(position,str):
        position = LazyExpr(position)
    if isinstance(position,LazyExpr):
        position = position.get(dictunion({"SW":sw,
                                 "SH":sh,
                                 "HSW":sw//2,
                                 "HSH":sh//2,
                                 "WW":ww,
                                 "WH":wh,
                                 "HWW":ww//2,
                                 "HWH":wh//2},extra))
    position =  position[:2]
    rendersurface.blit(target,tuple(position))
