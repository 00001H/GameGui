import gamegui,pygame
from gamegui import StyleChange
from gamegui.color import *
gamegui.config_window(900,650)
win = gamegui.Window()
gamegui.setdeffont(gamegui.SysFont("Courier New",45))
pygame.display.set_caption("Text test")
t = gamegui.Entry("",800,600)
t.sch = []
colornames = "red lightblue green yellow white gray".split()
def sat(x):
    return displaycolor(saturate(x,0.88))
colors = tuple(map(sat,map(name2color,colornames)))
def refresh(*a,**k):
    t.textwidg.sch = []
    for i in range(len(t.ctx)):
        t.textwidg.sch.append(StyleChange(i,StyleChange.COLOR,colors[i%len(colors)]))
    t.textwidg.sch.append(StyleChange(len(t.ctx)+2,StyleChange.COLOR,(255,255,255)))
t.acbe = t.dcbe = refresh
refresh()
win.add(t,(0,0))
def frame(evts,frm,fps,rmod):
    win.fill(displaycolor(saturate(name2color("gray"),0.4)))
    win.update()
    gamegui.disp.update()
gamegui.start_loop(win,frame,60)
