"""Defines abstract classes."""
from ._utils import blank_of_size,UnhandleableEvent
from .disp import winmgr
from abc import *
from pygame import Surface
class Widget(metaclass=ABCMeta):
    """Abstract class Widget.

get_surface must return the surface to be displayed. If undisplayable,
raise NotImplementedError().

Must have attributes 'width' and 'height'.

place_at is not recommended to be overriden.
_handle_event should not be overriden. This enables the user to customize event handling.

get_extra will be called after get_surface to return the extra arguments to evaluate the
lazy expression(if any).May or may not be overriden.Default is to return an empty dict.

handle_event takes an event and handles it,and should return True if consumed,
False if not.

unfocusable returns a boolean to indicate whether it is unfocusable by mouse click or
not.

User may assign a function evh_override that takes 2 arguments(self,event)
to override the event handling behavior.
(Details see gamegui.set_handler_override)"""
    @abstractmethod
    def get_surface(self):
        raise NotImplementedError()
    def get_extra(self):
        return {}
    def handle_event(self,event):
        return False
    def _handle_event(self,event):
        if hasattr(self,"evh_override"):
            try:
                if self.evh_override(self,event):
                    return True
            except UnhandleableEvent:
                return False
        return self.handle_event(event)
    def unfocusable(self):
        return True
    def on_update(self,is_focused):
        pass
    def place_at(self,pos,displaysurface):
        winmgr.place(self.get_surface(),displaysurface,pos,self.get_extra())
    def blank(self):
        s = blank_of_size(self.width,self.height)
        s.fill((0,0,0,0))
        return s
class Transformation(Widget,metaclass=ABCMeta):
    """Abstract class Transformation.

Instances must be compatible with initializations of form
'SomeSubClass(target_widget,width,height,**opts)'.

Must have attribute 'target'.
"""
    def handle_event(self,evt):
        return self.target.handle_event(evt)
    def unfocusable(self,*a,**k):
        return self.target.unfocusable(*a,**k)
    def on_update(self,isfoc):
        return self.target.on_update(isfoc)
class PcmtMgr(Widget,metaclass=ABCMeta):
    """Abstract class PcmtMgr.(Placement Manager).

Must support add to add child widgets.
Subclasses must either store child widgets(with NO EXTRA INFORMATION) in the
_childs list(Note:may store extra information in other attributes), or override
the `childs` property to return the list of childs).
Must also support enumerate_childs to return an iterable of (child,position)
tuples. It is used by the default get_surface implementation and is assumed by a
number of other functions."""
    @abstractmethod
    def add(self,child):
        raise NotImplementedError()
    def get_surface(self):
        surf = self.blank()
        for widg,pos in self.enumerate_childs():
            widg.place_at(pos,surf)
        return surf
    @abstractmethod
    def enumerate_childs(self):
        raise NotImplementedError()
    @property
    def childs(self):
        return tuple(self._childs)
