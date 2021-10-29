import pygame,gamegui
from collections import deque
from pygame.locals import *
from math import sqrt
win = gamegui.window(800,600)
w = gamegui.Entry(align=gamegui.CENTER)
def frame(events,frame,fps,rmod):
    thefps = rmod.target_fps if (fps is None) else fps
    win.fill((0,0,0))
    for e in events:
        if e.type == KEYDOWN:
            w.handle_event(e)
    w.place_at((0,0),win)
##    w.addsec(1/thefps)
    gamegui.disp.update()
gamegui.start_loop(frame,fps=60)
pygame.quit()
exit()
