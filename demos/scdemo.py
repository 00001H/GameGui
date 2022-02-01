import gamegui,pygame
from gamegui import StyleChange
from gamegui.color import *
gamegui.config_window(900,650)
win = gamegui.Window()
gamegui.setdeffont(gamegui.SysFont("Courier New",45))
pygame.display.set_caption("Text test")
t = gamegui.Entry("",900,650,selbg=(255,0,0),selfg=123)
colornames = "red lightblue green yellow white gray".split()
def sat(x):
    return displaycolor(saturate(x,0.88))
colors = tuple(map(sat,map(name2color,colornames)))
pygame.key.set_repeat(300,60)
def refresh():
    t.textwidg.sch = []
    delta = int(t.sec*1.36)%len(colors)
    for i in range(len(t.ctx)):
        t.textwidg.sch.append(StyleChange(i,StyleChange.FG,
                                          colors[(i+delta)%len(colors)]))
    t.textwidg.sch.append(StyleChange(len(t.ctx)+2,StyleChange.FG,(255,255,255)))
win.add(t,(0,0))
def frame(evts,frm,fps,rmod):
    win.fill(displaycolor(saturate(name2color("gray"),0.4)))
    refresh()
    win.update()
    gamegui.disp.update()
gamegui.start_loop(win,frame,60)
