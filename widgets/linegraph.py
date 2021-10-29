from ..defaults import DEFAULT_FONT
from ..bases import Widget
from .._utils import getsysfont as getfont
from .text import Text
from pygame import Rect
from pygame.draw import lines
from math import ceil
from collections import deque
from decimal import Decimal
def _startingfrom(ind,iterable):
    iterat = iter(iterable)
    try:
        for i in range(ind):
            next(iterat)
        while True:
            yield next(iterat)
    except StopIteration:
        return
class LineGraph(Widget):
    """A simple linear graph display.
Does not support log-log graph."""
    def __init__(self,array=None,w=300,h=200,wscale=1,dath=None,thickness=3,
                 color=(255,255,255),dyntop=0,scalewidth=0,sfs=10,resolution=1,scalepwr=10):
        """Initialize the graph.

Params(Note:Decimal objects can replace floats here):
array:None or deque(deque is recommended since it has fast popfront() but any sequence \
is ok.(do NOT pass iterator))of float|The data.
w,h:int|The width and height of the graph display.
wscale:float|The scale applied to the index of array to get the X-coordinate.
dath:None or float|The value at the top of the graph.If none,dynamically adjusts the scale.
thickness:int|The thickness,in pixels,of the lines.
color:3/4-tuple of int|The color of the lines(and the scale).
dyntop:int|The value added to the maximum of array for dynamic scaling.
scalewidth:int|The width of the scale at the left.0 hides the scale.
sfs:int|The font size of the scale.
resolution:int|The ratio of points to keep when displaying points.Should not exeed 1.
scalepwr:int|The power of the scale.

A lower resolution improves performance,but might have flashes.

The scale's numbers are linear,which means you'll see
1 2 3 6 9 18
instead of
1 3 9 27 81 243
for a scale power of 3.Log-log graphs are not supported."""
        self.array = deque() if (array is None) else array
        self.tkn = thickness
        self.color = color
        self.width = w
        self.height = h
        self.wscale = wscale
        self.dath = dath
        self.sw = scalewidth
        self.sfs = sfs
        self.dyntop = Decimal(dyntop)
        self.every = 1//resolution
        self.pwr = scalepwr
        self._thefont = getfont("Courier",sfs,"")
    def get_max_fit(self):
        """Returns the amount of points that can fit in one screen,
based on the scale width,widget width,and wscale.

If the array is longer than this value,you can delete the oldest values if you don't \
need them,to save memory."""
        return ceil((self.width-self.sw)*self.wscale)
    def get_surface(self):
        sf = self.blank()
        ignores = len(self.array)-self.get_max_fit()
        array = list(map(Decimal,_startingfrom(ignores,self.array)))
        maxy = (max(array)+self.dyntop if len(array) else 100) if (self.dath is None)\
               else self.dath
        scale = maxy/self.height
        if self.sw:
            sf.fill(self.color,Rect(self.sw-1,0,1,self.height))
            unit = 1
            while unit*self.pwr<maxy:
                unit *= self.pwr
            for i in range(0,ceil(maxy),unit):
                y = self.height-i//scale
                Text(str(i),self.sw-2,self.height,self.color,self._thefont).place_at(\
                    f"(1,{y}-{'$HTH' if i>0 else '$TH'})",sf)
        if len(array)==0:
            return sf
        pts = []
        for i,tem in enumerate(array):
            if i%self.every != 0:
                continue
            pts.append((round(i/self.wscale+self.sw),round(self.height-tem/scale)))
        if len(pts)==1:
            pts.append(pts[0])
        lines(sf,self.color,False,pts,self.tkn)
        return sf
