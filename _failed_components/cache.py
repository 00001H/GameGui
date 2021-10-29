"""Unsupported module.
The modules is a FAILED attempt at font caching.
You should NOT use it unless you strictly need this behavior.
Use the inspect module to find the source.
"""
from ._utils import SizedDict
class FontCache:
    def __init__(self):
        self.cache = SizedDict(20)
        self.fmisses = 0
        self.fhits = 0
        self.cmisses = SizedDict(20)
        self.chits = SizedDict(20)
    def getfor(self,font,char,aa,color):
        if font not in self.cache:
            self.fmisses += 1
            self.cmisses[font] = 0
            self.chits[font] = 0
            self.cache[font] = SizedDict(300)
        else:
            self.fhits += 1
        if char not in self.cache[font]:
            self.cache[font][char] = font.render(char,aa,color)
            self.cmisses[font] += 1
        else:
            self.chits[font] += 1
        return self.cache[font][char].copy()
    def statistics(self):
        return (self.fmisses,self.fhits,self.csmisses,self.chits)
    def __str__(self):
        rslt = f"FontCache("
        for attr in "fmisses fhits cmisses chits".split():
            rslt += f"{attr}={getattr(self,attr)}"
        rslt += ")"
        return rslt
fontCache = FontCache()
