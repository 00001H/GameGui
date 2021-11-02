from .bases import Transformation as Trans
from pygame.transform import scale,smoothscale
from pygame import Rect
class Crop(Trans):
    """Crops the target to a specific dimension."""
    def __init__(self,targetwidget,w,h):
        self.target = targetwidget
        self.width = w
        self.height = h
    def get_surface(self):
        b = self.blank()
        self.target.place_at((0,0),b)
        return b
Clamp = Crop
class Scale(Trans):
    """Scales the target to a specific dimension.
antialiased specifies whether the scaling algorithm should be fast or antialiased.

WARNING:Events won't be scaled!Use with interacting widgets at your own risk."""
    def __init__(self,targetwidget,w,h,antialiased=True):
        self.target = targetwidget
        self.width = w
        self.height = h
        self.aa = antialiased
    def get_surface(self):
        func = (smoothscale if self.aa else scale)
        return func(self.target.get_surface(),(self.width,self.height))
class Background(Trans):
    def __init__(self,targetwidget,w=None,h=None,color=(0,0,0,255)):
        self.target = targetwidget
        self._width = w
        self._height = h
        self.fillcolor = color
    @property
    def width(self):
        return self.target.width if (self._width is None) else self._width
    @width.setter
    def width(self,newv):
        self._width = newv#no adaptions now
    @property
    def height(self):
        return self.target.height if (self._height is None) else self._height
    @height.setter
    def height(self,newv):
        self._height = newv
    def get_surface(self):
        s = self.blank()
        s.fill(self.fillcolor)
        s.blit(self.target.get_surface(),(0,0))
        return s
class Boxed(Trans):
    def __init__(self,targetwidget,w,h,boxw=2,color=(0,0,0,255)):
        self.target = targetwidget
        self.width = w
        self.height = h
        self.cl = color
        self.bw = boxw
    def get_surface(self):
        s = self.blank()
        s.blit(self.target.get_surface(),(0,0))
        s.fill(self.cl,Rect(0,0,self.width,self.bw))
        s.fill(self.cl,Rect(0,self.height-self.bw,self.width,self.bw))
        s.fill(self.cl,Rect(0,0,self.bw,self.height))
        s.fill(self.cl,Rect(self.width-self.bw,0,self.bw,self.height))
        return s
class Origined(Trans):
    """Crops the target to a specific dimension."""
    def __init__(self,targetwidget,w,h):
        self.target = targetwidget
        self.width = w
        self.height = h
    def get_surface(self):
        b = self.blank()
        t = self.target
        self.target.place_at((t.width-self.width,t.height-self.height),b)
        return b
