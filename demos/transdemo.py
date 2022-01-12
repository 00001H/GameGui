import pygame,gamegui
from gamegui.transform import Scale,Crop,Background,Boxed,Origined
from collections import deque
from pygame.locals import *
from math import sqrt
gamegui.config_window(800,600)
win = gamegui.Window()
ent = gamegui.Entry(align=gamegui.CENTER,antialiased=True)
ent2 = gamegui.Entry(align=gamegui.CENTER,antialiased=True)
win.add(
        Boxed(
              Background(ent,w=400,h=600,color=(220,170,80)),
              400,600,
              2,(255,0,0)
        ),
        (0,0)
)
win.add(
        Boxed(
              Background(ent2,w=400,h=600,color=(220,170,80)),
              400,600,
              2,(255,0,0)
        ),
        (400,0)
)
pygame.key.set_repeat(300,68)
def frame(events,frame,fps,rmod):
    thefps = rmod.target_fps if (fps is None) else fps
    win.fill((0,0,0))
    win.update()
    gamegui.disp.update()
gamegui.start_loop(win,frame,fps=60)
pygame.quit()
exit()
