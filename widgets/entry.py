"""The Entry class."""
from ..bases import Widget
from .._utils import getmods
from .text import Text
from pygame import Surface
from time import time
from pygame.locals import *
class Entry(Widget):
    """Text input box.
text specifies default text,
w and h specifies dimensions.
Other options are same as the Text widget."""
    def __init__(self,text="",w=500,h=500,*a,**k):
        self.ctx = list(text)
        self.textwidg = Text("",w,h,*a,**k)
        self.cursor = 0
        self.sec = 0
    @property
    def width(self):
        return self.textwidg.width
    @width.setter
    def width(self,value):
        self.textwidg.width = value
    @property
    def height(self):
        return self.textwidg.height
    @height.setter
    def height(self,value):
        self.textwidg.height = height
    def settext(self,text):
        self.textwidg.content = text
    def handle_event(self,event):
        if event.type == KEYDOWN:
            self._handle(event)
            return True
        return False
    def on_update(self,foc):
        self.sec = time() if foc else 0
    def _handle(self,evt):#MUST HAVE PROPERTIES unicode,key
        if getmods(evt).ctrl:
            return#control-* should not be handled
        if evt.key == K_BACKSPACE:
            if self.cursor != 0:
                del self.ctx[self.cursor-1]
                self.cursor -= 1
        elif evt.key == K_RETURN:#evt.unicode will be "\r" not "\n"
            self.ctx.insert(self.cursor,"\n")
            self.cursor += 1
        elif evt.key == K_DELETE:
            if self.cursor < len(self.ctx):
                del self.ctx[self.cursor]
        elif evt.key == K_LEFT:
            if self.cursor > 0:
                self.cursor -= 1
        elif evt.key == K_RIGHT:
            if self.cursor < len(self.ctx):
                self.cursor += 1
        elif evt.unicode:
            self.ctx.insert(self.cursor,evt.unicode)
            self.cursor += 1
    def get_surface(self):
        ctx = list(self.ctx)
        self.textwidg.cursor = -1
        if int(self.sec*1.36)%2 == 1:
            self.textwidg.cursor = self.cursor
        self.textwidg.settext("".join(ctx))
        return self.textwidg.get_surface()
