import pygame
from ._utils import RuntimeModifiable as RMod
from .bases import Transformation,PcmtMgr
from pygame import KEYDOWN,K_ESCAPE,K_F11,MOUSEBUTTONDOWN
from .disp.winmgr import getrect
__all__ = ["EventMgr","start_loop"]
class _NodeWrapper:
    def __init__(self,node,par,dct=None):
        self.n = node
        self.parent = par
        self._dct = {} if (dct is None) else dct
    def __getattr__(self,attr):
        if attr in self._dct:
            return self._dct[attr]
        return getattr(self.n,attr)
def _walk_nodes(where,node,par=None):#Really should define it in _utils.
    if isinstance(node,Transformation):
        nw = _NodeWrapper(node.target,par,{"width":node.width,"height":node.height})
    else:
        nw = _NodeWrapper(node,par)
    if isinstance(node,PcmtMgr):
        for chld,subwhere in node.enumerate_childs():
            yield from _walk_nodes(subwhere,chld,nw)
    yield (nw,where)
class EventMgr:
    """Event Manager."""
    def __init__(self,window):
        self.w = window
        window.focused_widget = None
    def handle_events(self,evts=None):
        """Handles the events.If None(default),grabs from pygame.event.get().
Removes events that are processed."""
        if evts is None:
            evts = pygame.event.get()
        evtscpy = list(evts)
        for evt in evtscpy:#won't say list size changed during iteration then
            if evt.type == MOUSEBUTTONDOWN:
                for widg,pos in _walk_nodes((0,0),self.w):
                    if (widg.n is self.w) or widg.unfocusable():
                        continue
                    rec = pygame.Rect(*getrect(widg,pos,widg.get_extra()),widg.width,
                                      widg.height)
                    if rec.collidepoint(evt.pos):
                        self.w.focused_widget = widg
            if self.w.focused_widget is not None:
                current = self.w.focused_widget
                while not current.handle_event(evt):#keep going parent if can't handle
                    current = current.parent#move up a level
                    if current.n is self.w:#no handler
                        break
                else:#loop-else triggers if not stopped with a break statement
                    evts.remove(evt)#found handler;delete event
def start_loop(win,callback,fps=60,no_quit=False,evm=None):
    """Starts the event loop.
args:
win: the window
callback: the callback called to display each frame. It should update the display as this
function will not do it by default.
no_quit: if True, will not quit the event loop if pygame.QUIT event is generated(by
clicking the X or calling pygame.event.put())
evm: The event manager. Will create a new one by default.

Callback should accept 4 arguments: the event list, the current frame, the current
fps(as returned by clock.get_fps(), will be 0 for the first 10 frames), and a
RuntimeModifiable that is basically a class with no methods and limited to some attributes.
The callback may fetch it or change it by using
runtimemodifiable.field [= new]

Current attributes: target_fps     the target fps(passed in the fps argument when starting
the loop)"""
    should_stop = False
    clk = pygame.time.Clock()
    frame = 0
    data = RMod(["target_fps"])
    data.target_fps = fps
    if evm is None:
        evm = EventMgr(win)
    while True:
        events = []
        for event in pygame.event.get():
            if (not no_quit) and event.type == pygame.QUIT:
                should_stop = True
                break
            events.append(event)
        evm.handle_events(events)
        if data.target_fps == -1:
            clk.tick()
        else:
            clk.tick(data.target_fps)
        currfps = clk.get_fps()
        if frame < 10:
            currfps = None
        if should_stop or callback(events,frame,currfps,data):
            break
        frame += 1
