"""Utility module."""
from .mast import literal_eval as _le
from pygame import locals as lc,Surface
from pygame.font import match_font,Font,SysFont
from collections import namedtuple as nt,deque
def focused_in(x):return getattr(x,"focused_widget",None)
def getdeffont():
    """Returns the default font."""
    return DEFFONT
def setdeffont(fnt):
    """Sets the default font to a new font."""
    global DEFFONT
    DEFFONT = fnt
class _NodeWrapper:
    def __init__(self,node,par,dct=None):
        self.n = node
        self.parent = par
        self._dct = {} if (dct is None) else dct
    def __getattr__(self,attr):
        if attr in self._dct:
            return self._dct[attr]
        return getattr(self.n,attr)
def walk_nodes(where,node,par=None):
    from .bases import PcmtMgr,Transformation
    if isinstance(node,Transformation):
        wid = node.width
        ht = node.height
        while isinstance(node,Transformation):
            node = node.target
        nw = _NodeWrapper(node,par,{"width":wid,"height":ht})
    else:
        nw = _NodeWrapper(node,par)
    if isinstance(node,PcmtMgr):
        for chld,subwhere in node.enumerate_childs():
            yield from walk_nodes(subwhere,chld,nw)
    yield (nw,where)
class FontBase(Font):
    """Internal class.
All methods and attributes subject to change.
Not initialized directly,instead pass FontBase.construct to the constructor parameter
of the font constructors to enable correct equality testing and hashing."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.properties = (args,tuple(kwargs.items()))
    def __hash__(self):
        return hash(self.properties)
    def __eq__(self, other):
        return self.properties == other.properties
    @classmethod
    def construct(cls,fontpath,size,bold,italic):
        font = cls(fontpath,size)
        font.strong = bold
        font.oblique = italic
        return font
class LazyExpr:
    """Lazy expression.
Replaces the $KEY with VALUE for key-value pairs in parameter dic.
VALUE must be a string."""
    def __init__(self,expr):
        self.value = expr
    def get(self,dic):
        va = self.value
        for key in dic:
            va = va.replace("$"+key,repr(dic[key]))
        return _le(va)
class Opts:
    """Internal class.
Allows multiple options in one value.
EXAMPLE:

YES = 0b1
NO = 0b10
DISPLAY_NOW = 0b100
HAS_BOOLEAN = Opts(YES,NO)

CONFIG = YES|DISPLAY_NOW

assert     CONFIG        &  HAS_BOOLEAN
assert     NO            &  HAS_BOOLEAN
assert not DISPLAY_NOW   &  HAS_BOOLEAN"""
    def __init__(self,*opts):
        self.opts = opts
    def __rand__(self,val):
        for opt in self.opts:
            if val&opt:
                return True
        return False
class RuntimeModifiable:
    """Internal class to store attributes.Can be passed to functions to change configs.
Subject to change."""
    def __init__(self,slots):
        self.dic = dict.fromkeys(slots)
    def __setattr__(self,attr,value):
        if attr != "dic":
            self.dic[attr] = value
        else:
            super().__setattr__(attr,value)
    def __getattr__(self,attr):
        if attr in self.dic:
            return self.dic[attr]
        raise AttributeError()
class SizedDict:
    """Sized dict for efficient caching. If full,removes the least-recently-used item."""
    def __init__(self,cap):
        self.cap = cap
        self.internal = {}
        self.updated = deque()
        self.full = False
    def _miss(self,item,value):
        if not self.full:
            if len(self.internal) == self.cap:
                self.full = True
        if self.full:
            del self.internal[self.updated.popleft()]
            self.internal[item] = value
        else:
            self.internal[item] = value
        self.updated.append(item)
    def __contains__(self,item):
        return item in self.internal
    def __len__(self):
        return len(self.internal)
    def __setitem__(self,item,value):
        if item not in self.internal:
            self._miss(item,value)
        else:
            self.internal[item] = value
            if item in self.updated:
                ind = self.updated.index(item)
                if ind+1 != len(self.updated):
                    self.updated.pop(ind)
                    self.updated.append(item)
            else:
                raise RuntimeError(f"{item} not in self.updated({self.updated})")
    def __getitem__(self,item):
        return self.internal[item]
    def __str__(self):
        return f"SizedDict[{self.cap}]({self.internal})"
def blank_of_size(w,h):
    """Get a fully transparent surface supporting per-pixel alpha of size (w,h)."""
    s = Surface((w,h)).convert_alpha()
    s.fill((0,0,0,0))
    return s
def dictunion(x,y):
    """merges two dicts.
y takes priority for duplicate keys."""
    cop = x.copy()
    cop.update(y)
    return cop
SHIFTMOD = Opts(1,2)
CTRLMOD = Opts(64,128)
ALTMOD = Opts(256,512)
WINMOD = Opts(1024,2048)
NUMLOCKMOD = 4096
CAPSLOCKMOD = 8192
_mods = nt("keymods","ctrl shift alt capslock numlock windows".split())
def getmods(evt):
    """Calculates modifier key presses from an event.
Returns a namedtuple 'keymods' with attributes
ctrl,shift,alt,capslock,numlock,windows"""
    mod = evt.mod
    return _mods(mod&CTRLMOD,mod&SHIFTMOD,mod&ALTMOD,mod&CAPSLOCKMOD,
                 mod&NUMLOCKMOD,mod&WINMOD)

def getsysfont(*a,**k):
    """Gets a system font. Supports correct equality testing and hashing."""
    return SysFont(*a,constructor=FontBase.construct,**k)
def getfont(*a,**k):
    """Gets a font from path. Supports correct equality testing and hashing."""
    return Font(*a,constructor=FontBase.construct,**k)
DEFFONT = getsysfont("Courier New",22,"bold")
