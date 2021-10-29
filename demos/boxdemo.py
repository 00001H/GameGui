import pygame,gamegui
from collections import deque
from pygame.locals import *
from math import sqrt
gamegui.config_window(800,600)
win = gamegui.Window()
ent = gamegui.Entry(align=gamegui.CENTER)
win.add((0,0),ent)
def frame(events,frame,fps,rmod):
    thefps = rmod.target_fps if (fps is None) else fps
    win.fill((0,0,0))
    win.update()
    ent.addsec(1/thefps)
    gamegui.disp.update()
gamegui.start_loop(win,frame,fps=60)
pygame.quit()
exit()
