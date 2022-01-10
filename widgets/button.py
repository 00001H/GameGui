"""The button widget."""
from ..bases import Widget
from .text import Text
from pygame import MOUSEBUTTONDOWN
class Button(Widget):
    def __init__(self,w,h,text,*a,action=(lambda evt:None),**k):
        self.width = w
        self.height = h
        self.text = text
        self.action = action
    @property
    def text(self):
        return self._texw.content
    @text.setter
    def text(self,new):
        self._texw.content = new
    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.action(event)
            return True
        return False
    def get_surface(self):
        sf = self.blank()
        sf.blit(self._texw.get_surface(),(0,0))
        return sf
