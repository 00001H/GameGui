"""The Text widget."""
from ..defaults import DEFAULT_FONT
from ..bases import Widget
from .._utils import blank_of_size
from pygame.font import SysFont as getfonts
LEFT = object()#unique
CENTER = object()
RIGHT = object()
class Text(Widget):
    """A text label.
text specifies initial text,
w,h specifies dimensions,
color specifies the text color(foreground),
font specifies the font to use,
antialiased specifies if antialiasing should be enabled,
align specifies the align style(LEFT,CENTER,RIGHT), and
linespacing specifies the space between lines."""
    def __init__(self,text="",w=500,h=500,
                 color=(255,255,255),font=DEFAULT_FONT,antialiased=True,
                 align=LEFT,linespacing=1):
        self.content = text
        self.font = font
        self.color = color
        self.aa = antialiased
        self.align = align
        self.width = w
        self.height = h
        self.cursor = -1
        self.lsp = linespacing
    def settext(self,text):
        self.content = text
    def get_surface(self):
        lines = []
        ht = 0
        i = 0
        cursor = None
        cotl = self.cursor
        whereisthecursor = 0
        for lnc,line in enumerate(self.content.split("\n")):
            small = i<self.cursor
            if i==self.cursor:
                whereisthecursor = lnc
                cursor = (0,ht)
            ln = self.font.render(line,self.aa,self.color)
            i += len(line)+1
            if (cursor is None) and small and i>self.cursor:
                whereisthecursor = lnc
                ratio = ln.get_rect().width/len(line)
                cursor = (int(cotl*ratio),ht)
            cotl -= len(line)+1
            lines.append((ln,ht))
            ht += ln.get_rect().height+self.lsp
        charh = ln.get_rect().height
        if ht:
            ht -= self.lsp
        if (cursor is None) and self.cursor!=-1:
            cursor = (ln.get_rect().width,ht-charh)
            whereisthecursor = lnc
        sf = self.blank()
        self.TH = ht
        self.HTH = ht//2
        xdiff = 0
        for i,(lnsf,y) in enumerate(lines):
            if self.align is LEFT:
                x = 0
            elif self.align is CENTER:
                rect = lnsf.get_rect()
                rect.centerx = self.width//2
                x = rect.left
            elif self.align is RIGHT:
                rect = lnsf.get_rect()
                rect.right = self.width
                x = rect.left
            else:
                raise ValueError(f"Invalid align:{self.align}")
            if cursor is not None and whereisthecursor == i:
                xdiff = x
            sf.blit(lnsf,(x,y))
        if cursor is not None:
##            print("Displaying with XDIFF",xdiff,"'Cause",lnsf.get_rect().width)
            sf.fill(self.color,(cursor[0]+xdiff,cursor[1],2,charh))
        return sf
    def get_extra(self):
        return {"TH":self.TH,"HTH":self.HTH}
