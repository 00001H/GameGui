import pygame
from .._utils import RuntimeModifiable as RMod
from pygame import KEYDOWN,K_ESCAPE,K_F11,MOUSEBUTTONDOWN
__all__ = ["EventMgr","start_loop"]
class EventMgr:
    """Event Manager."""
    def __init__(self,window):
        self.w = window
        window.focused_widget = None
    def handle_events(self,evts=None):
        """Handles the events.If None(default),grabs from pygame.event.get()."""
        if evts is None:
            evts = pygame.event.get()
        for evt in evts:
            if evt.type == MOUSEBUTTONDOWN:
                for pos,widg in self.w._childs:
                    if widg.unfocusable():
                        continue
                    rec = pygame.Rect(pos[0],pos[1],widg.width,widg.height)
                    if rec.collidepoint(evt.pos):
                        if self.w.focused_widget == widg:
                            self.w.focused_widget.handle_event(evt)
                        else:
                            self.w.focused_widget = widg
            else:
                if self.w.focused_widget is not None:
                    self.w.focused_widget.handle_event(evt)
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
