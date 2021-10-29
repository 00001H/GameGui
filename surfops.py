from .bases import Widget
from pygame.transform import scale,smoothscale
class Crop(Widget):
    def __init__(self,targetwidget,w,h):
        self.t = targetwidget
        self.width = w
        self.height = w
    def get_surface(self):
        b = self.blank()
        self.t.place_at((0,0),b)
        return b
class Scale(Widget):
    def __init__(self,targetwidget,w,h,antialiased=True):
        self.t = targetwidget
        self.width = w
        self.height = w
        self.aa = antialiased
    def get_surface(self):
        func = (smoothscale if self.aa else scale)
        return func(self.t.get_surface(),(self.width,self.height))
