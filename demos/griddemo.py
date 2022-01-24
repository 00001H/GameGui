"""Conway's Game Of Life, by 00001H"""
import pygame,gamegui
from collections import deque
from pygame.locals import *
from math import sqrt
gamegui.config_window(1100,600)
win = gamegui.Window()
gr = gamegui.Grid(1100,600,20,20,600,600,borderw=1,bordercolor=(151,151,151))
LIVE = gamegui.Background(gamegui.NULLWIDGET,20,20,(240,240,0))
DEAD = gamegui.NULLWIDGET
win.add(gamegui.Background(gr,color=(126,126,126)),(0,0))
def frame(events,frame,fps,rmod):
    win.update()
    gamegui.disp.update()
gamegui.start_loop(win,frame,fps=60)
pygame.quit()
exit()
