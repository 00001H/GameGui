"""The button widget."""
from ..bases import Widget
from .text import Text
from pygame import MOUSEBUTTONDOWN
class Button(Widget):
    """A rectangular button widget.

Arguments:
w,h: Dimensions of the button
text: The label text of the button
*Any more positional arguments are passed to the label Text widget constructor

Keyword arguments:
action: The function run on click. Should accept one argument, the MOUSEBUTTONDOWN event.
Does nothing by default.
**Any more keyword arguments are passed to the label Text widget constructor

Note: Supports the positioning specifier $TW,$TH,$HTW,$HTH obtained from the Text.
However, the button's clickable area is still the whole widget, not the text."""
    def __init__(self,w,h,text,*a,action=(lambda evt:None),**k):
        self.width = w
        self.height = h
        self._texw = Text(text,w,h,*a,**k)
        self.text = text
        self.action = action
    @property
    def text(self):
        return self._texw.content
    @text.setter
    def text(self,new):
        self._texw.content = new
    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.action(event)
            return True
        return False
    def get_surface(self):
        sf = self.blank()
        sf.blit(self._texw.get_surface(),(0,0))
        return sf
    def get_extra(self):
        return self._texw.get_extra()
