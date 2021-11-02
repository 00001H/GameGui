from ._utils import SizedDict
class CWCache:
    def __init__(self):
        self.cache = SizedDict(200)
        self.fmisses = 0
        self.fhits = 0
        self.cmisses = SizedDict(200)
        self.chits = SizedDict(200)
    def get(self,font,char,aa):
        if font not in self.cache:
            self.fmisses += 1
            self.cmisses[font] = 0
            self.chits[font] = 0
            self.cache[font] = SizedDict(1000)
        else:
            self.fhits += 1
        if char not in self.cache[font]:
            self.cache[font][char] = font.render(char,aa,(0,0,0)).get_rect().width
            self.cmisses[font] += 1
        else:
            self.chits[font] += 1
        return self.cache[font][char]
    def statistics(self):
        return (self.fmisses,self.fhits,self.csmisses,self.chits)
    def __str__(self):
        rslt = f"FontCache("
        for attr in "fmisses fhits cmisses chits".split():
            rslt += f"{attr}={getattr(self,attr)},"
        rslt = rslt.rstrip(",")
        rslt += ")"
        return rslt
cwc = CWCache()
