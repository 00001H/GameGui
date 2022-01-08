from os import walk
from os.path import join
mods = []
for currr,subd,subf in walk(".."):
    if "." in currr:
        continue
    curr = currr[currr.find("gamegui"):]
    curr = curr.replace("\\","/").replace("/",".")
    mods.append(curr)
    for f in subf:
        if f.endswith(".py") and f != "__init__.py" and ("demo" not in f):
            mods.append(curr+"."+f[:-3])
def x():pass
class Foo:
    def bar(self):pass
functype = type(x)
mthtype = type(Foo.bar)
for mod in mods:
    dic = vars(__import__(mod))
    for k,v in dic.items():
        if isinstance(v,(functype,mthtype,type)):
            if not getattr(v,"__doc__",""):
                print(f"You should document {mod}.{k}")
input()
