import pygame
from ._utils import RuntimeModifiable as RMod,_NodeWrapper,walk_nodes
from pygame import KEYDOWN,K_ESCAPE,K_F11,MOUSEBUTTONDOWN
from .disp.winmgr import getrect
__all__ = ["EventMgr","start_loop"]
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
                handle = True
                for widg,pos in walk_nodes((0,0),self.w):
                    if (widg.n is self.w):
                        continue
                    rec = pygame.Rect(*getrect(widg,pos,widg.get_extra()),widg.width,
                                      widg.height)
                    if rec.collidepoint(evt.pos):
                        if handle and widg._handle_event(evt):
                            handle = False
                        if not widg.unfocusable():
                            self.w.focused_widget = widg
            else:
                if self.w.focused_widget is not None:
                    current = self.w.focused_widget
                    while not current._handle_event(evt):#keep going parent if can't handle
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
