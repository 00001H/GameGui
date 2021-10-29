import pygame
from ._utils import RuntimeModifiable as RMod
from .widgets import XYPcmtMgr
from pygame import KEYDOWN,K_ESCAPE,K_F11,MOUSEBUTTONDOWN
__all__ = ["EventMgr","start_loop"]
class _NodeWrapper:
    def __init__(self,node,par):
        self.n = node
        self.parent = par
    def __getattr__(self,attr):
        return getattr(self.n,attr)
def _walk_nodes(where,node,par=None):#Really should define it in _utils.
    #WARNING:Only works on XYPcmtMgr.Planning to support other placement
    #managers with a get_where() method.
    #Won't add rn because it's too complicated.
    nw = _NodeWrapper(node,par)
    if isinstance(node,XYPcmtMgr):
        for subwhere,chld in node._childs:
            yield from _walk_nodes(subwhere,chld,nw)
    yield (where,nw)
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
            isvalid = True
            if evt.type == MOUSEBUTTONDOWN:
                for pos,widg in _walk_nodes((0,0),self.w):
                    if (widg.n is self.w) or widg.unfocusable():
                        continue
                    rec = pygame.Rect(pos[0],pos[1],widg.width,widg.height)
                    if rec.collidepoint(evt.pos):
                        if self.w.focused_widget != widg:
                            self.w.focused_widget = widg
                            isvalid = False#the "focusing" click should be ignored
            if isvalid:
                if self.w.focused_widget is not None:
                    current = self.w.focused_widget
                    while not current.handle_event(evt):#keep going parent if can't handle
                        current = current.parent#move up a level
                        if current.n is self.w:#no handler
                            break
                    else:#loop-else triggers if not stopped with a break statement
                        evts.remove(evt)#found handler;delete event
def start_loop(win,callback,fps=60,quit_on_esc=False,no_quit=False,evh=None):
    should_stop = False
    clk = pygame.time.Clock()
    frame = 0
    data = RMod(["target_fps"])
    data.target_fps = fps
    if evh is None:
        evh = EventMgr(win)
    while True:
        events = []
        for event in pygame.event.get():
            if (not no_quit) and event.type == pygame.QUIT:
                should_stop = True
                break
            if event.type == KEYDOWN:
                if quit_on_esc and event.key == K_ESCAPE:
                    should_stop = True
                    break
            events.append(event)
        evh.handle_events(events)
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
