import pygame,gamegui
from collections import deque
from pygame.locals import *
from gamegui.defaults import DEFAULT_FONT as df
from math import sqrt
win = gamegui.window(1100,600)
g = gamegui.LineGraph(None,1100,400,scalewidth=80,sfs=15,scalepwr=40)
x = deque()
def div(x,y):
    if y==0:
        return 0
    return x/y
tolerance = 100
value = 2
def frame(events,frame,fps,rmod):
    global tolerance,value
    win.fill((121,212,121))
    x.append(value)
    value *= (1.0001+sqrt(sqrt(sqrt(value/1000)/1000)/1000))
    if value == float("inf"):
        value = 9162.738597
    if len(x)>g.get_max_fit():
        x.popleft()
    g.array = x
    g.place_at("($HSW-$HWW,100)",win)
    gamegui.disp.update()
gamegui.start_loop(frame,fps=60)
pygame.quit()
exit()
