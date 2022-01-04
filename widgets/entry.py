"""The Entry class."""
from ..bases import Widget
from .._utils import getmods
from .text import Text
from pygame import Surface
from time import time
from pygame.locals import *
def _nullfunc(*a,**k):pass
class Entry(Widget):
    """Text input box.
text specifies default text,
w and h specifies dimensions.
Other options are same as the Text widget."""
    def unfocusable(self):
        return False
    def __init__(self,text="",w=500,h=500,*a,**k):
        self.ctx = list(text)
        self.textwidg = Text("",w,h,*a,**k)
        self._cursor = 0
        self.sec = 0
        self.acb = self.acbe = self.dcb = self.dcbe = _nullfunc
    @property
    def cursor(self):
        return self._cursor
    @cursor.setter
    def cursor(self,new):
        self._cursor = max(0,min(len(self.ctx),new))
    @property
    def width(self):
        return self.textwidg.width
    @width.setter
    def width(self,value):
        self.textwidg.width = value
    @property
    def height(self):
        return self.textwidg.height
    @property
    def text(self):
        return "".join(self.ctx)
    @text.setter
    def text(self,new):
        self.ctx = list(new)
        self.cursor = min(self.cursor,len(self.ctx))
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
    def _addch(self,ch,move=True):
        self.acb(self,ch,move)
        self.ctx.insert(self.cursor,ch)
        if move:
            self.cursor += 1
        self.acbe(self,ch,move)
    def _rmch(self):
        self.dcb(self)
        if self.cursor > 0:
            del self.ctx[self.cursor-1]
        self.dcbe(self)
    def _bksp(self):
        self._rmch()
        self.cursor -= 1
    def _delkey(self):
        self.cursor += 1
        self._bksp()
    def _addstr(self,st,move=True):
        for ch in st:
            self._addch(self,ch,move)
    def _handle(self,evt):#MUST HAVE PROPERTIES unicode,key
        if getmods(evt).ctrl:
            return#control-* should not be handled
        if evt.key == K_BACKSPACE:
            self._bksp()
        elif evt.key == K_DELETE:
            self._delkey()
        elif evt.key == K_LEFT:
            self.cursor -= 1
        elif evt.key == K_RIGHT:
            self.cursor += 1
        elif evt.unicode:
            self._addch(evt.unicode.replace("\r","\n"))
    def get_surface(self):
        self.textwidg.cursor = -1
        if int(self.sec*1.36)%2 == 1:
            self.textwidg.cursor = self.cursor
        self.textwidg.settext(self.text)
        return self.textwidg.get_surface()
