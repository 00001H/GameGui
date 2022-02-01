"""The Entry class."""
import pyperclip
from ..bases import Widget
from .._utils import getmods
from .text import Text,StyleChange
from pygame import Surface
from time import time
from pygame.locals import *
def _nullfunc(*a,**k):pass
class BasicEntry(Widget):
    """Basic text input box.
text specifies default text,
w and h specifies dimensions.
Other options are same as the Text widget.

Supports:
Arrow keys to move cursor
Multi-line text
Basic Typing
All text operations(modify basicentry.textwidg to set options), to modify text,
assign to the "text" proeprty.(DON'T MODIFY THE CTX PROPERTY)"""
    def unfocusable(self):
        return False
    def __init__(self,text="",w=500,h=500,*a,**k):
        self.ctx = text
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
        return self.ctx
    @text.setter
    def text(self,new):
        self.ctx = new
        self.cursor = min(self.cursor,len(self.ctx))
    @height.setter
    def height(self,value):
        self.textwidg.height = height
    def settext(self,text):
        self.textwidg.content = text
    def handle_event(self,event):
        if event.type == KEYDOWN:
            return self._handle(event)
        return False
    def on_update(self,foc):
        self.sec = time() if foc else 0
    def _addch(self,ch,move=True):
        self.acb(self,ch,move)
        self.ctx = self.ctx[:self.cursor]+ch+self.ctx[self.cursor:]
        if move:
            self.cursor += 1
        self.acbe(self,ch,move)
    def _rmch(self):
        self.dcb(self)
        if self.cursor > 0:
            self.ctx = self.ctx[:self.cursor-1]+self.ctx[self.cursor:]
        self.dcbe(self)
    def backspace(self):
        """Handles the backspace key."""
        self._rmch()
        self.cursor -= 1
    def delete(self):
        """Handles the delete key."""
        self.cursor += 1
        self.backspace()
    def _addstr(self,st,move=True):
        for ch in st:
            self._addch(ch,move)
    def _handle(self,evt):#MUST HAVE PROPERTIES unicode,key
        if getmods(evt).ctrl:
            return False#control-* should not be handled
        if evt.key == K_BACKSPACE:
            self.backspace()
        elif evt.key == K_DELETE:
            self.delete()
        elif evt.key == K_LEFT:
            self.cursor -= 1
        elif evt.key == K_RIGHT:
            self.cursor += 1
        elif evt.unicode:
            self._addch(evt.unicode.replace("\r","\n"))
        else:
            return False
        return True
    def get_surface(self):
        self.textwidg.cursor = -1
        if int(self.sec*1.36)%2 == 1:
            self.textwidg.cursor = self.cursor
        self.textwidg.settext(self.text)
        return self.textwidg.get_surface()
class Entry(BasicEntry):
    """More advanced entry.

Arguments(in addition to BasicEntry's argument):
selbg/selfg: Selection color. Defaults to dark gray/None.

On top of BasicEntry's functionality, supports:
Cut/Copy/Paste via Ctrl-c,Ctrl-v and Ctrl-x
Selection support, Shift-arrow key to modify selection

Cursor selection coming soon!"""
    def __init__(self,*a,**k):
        self.selbg = k.get("selbg",(110,110,110))
        self.selfg = k.get("selfg",None)
        if "selbg" in k:
            del k["selbg"]
        if "selfg" in k:
            del k["selfg"]
        super().__init__(*a,**k)
        self.selection = None
        self.selstart = -1
    def get_surface(self):
        tw = self.textwidg
        if self.selection is not None:
            osch = list(tw.sch)
            if not ((self.selbg is None) and (self.selfg is None)):
                for i,tem in enumerate(osch):
                    if tem.where in range(*self.selection):
                        if ((self.selbg is not None) and\
                            (tem.k is StyleChange.BG)) or\
                           ((self.selfg is not None) and\
                            (tem.k is StyleChange.FG)):
                            tw.sch.remove(tem)
            if self.selbg is not None:
                prevbg = tw.bkgc
                for sc in tw.sch:
                    if sc.where < self.selection[0] and sc.k is StyleChange.BG:
                        prevbg = sc.n
                tw.sch.append(StyleChange(self.selection[0],StyleChange.BG,
                                          self.selbg))
                tw.sch.append(StyleChange(self.selection[1],StyleChange.BG,
                                          prevbg))
            if self.selfg is not None:
                prevfg = tw.color
                for sc in tw.sch:
                    if sc.where < self.selection[0] and sc.k is StyleChange.FG:
                        prevfg = sc.n
                tw.sch.append(StyleChange(self.selection[0],StyleChange.FG,
                                          self.selfg))
                tw.sch.append(StyleChange(self.selection[1],StyleChange.FG,
                                          prevfg))
        sfc = super().get_surface()
        if self.selection is not None:
            tw.sch = osch
        return sfc
    def backspace(self):
        """Handles the backspace key."""
        if self.selection is None:
            super().backspace()
        else:
            self.ctx = self.ctx[:self.selection[0]]+self.ctx[self.selection[1]:]
            self.cursor = self.selection[0]#self.cursor += 1 is ignored, so no
            self.selection = None          #need to override delete()
    def _addch(self,ch,move=True):
        if self.selection is not None:
            self.backspace()#remove selection
        super()._addch(ch,move)
    def _handle(self,evt):
        slct = self.selection
        cursor = self.cursor
        mds = getmods(evt)
        if mds.ctrl and (not mds.shift) and (not mds.alt):
            if evt.key == K_c:
                if slct is not None:
                    pyperclip.copy(self.ctx[slct[0]:slct[1]])
                    return True
            elif evt.key == K_v:
                self._addstr(pyperclip.paste().replace("\r\n","\n")\
                                              .replace("\r",""))#auto-override
                return True                                     #selection
        if mds.shift and (not mds.ctrl) and (not mds.alt):
            if evt.key == K_LEFT:
                if (slct is None) and (cursor>0):
                    slct = self.selection = [cursor-1,cursor]
                    self.selstart = 1
                else:
                    slct[1-self.selstart] -= 1
                    if slct[0]>slct[1]:
                        slct = list(reversed(slct))
                        self.selstart = 1-self.selstart
                if slct[0]==slct[1]:
                    slct = self.selection = None
                self.cursor -= 1
                return True
            elif evt.key == K_RIGHT:
                if (slct is None) and (cursor<len(self.ctx)):
                    slct = self.selection = [cursor,cursor+1]
                    self.selstart = 0
                else:
                    slct[1-self.selstart] += 1
                    if slct[0]>slct[1]:
                        slct = list(reversed(slct))
                        self.selstart = 1-self.selstart
                if slct[0]==slct[1]:
                    slct = self.selection = None
                self.cursor += 1
                return True
        if (not mds.ctrl) and (not mds.shift) and (not mds.alt):
            if evt.key in (K_LEFT,K_RIGHT):
                self.selection = None#un-shift-ed move
        return super()._handle(evt)
