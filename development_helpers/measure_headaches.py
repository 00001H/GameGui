from os import walk
from os.path import join
lines = chars = files = 0
encs = "ascii utf-8 utf-16 latin-1".split()
lib = ".."
for curr,subd,subf in walk(lib):
    for fn in subf:
        full = join(curr,fn)
        if full.lower().endswith(".py") or full.lower().endswith(".pyw"):
            for enc in encs:
                try:
                    f = open(full,encoding=enc)
                    tex = f.read()
                except UnicodeError:
                    pass
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass
                else:
                    f.close()
                    break
            else:
                print(f"Cannot decode: {full}")
            files += 1
            for ln in tex.splitlines():
                ln = ln.replace(" ","")
                lines += 1
                chars += len(ln)
print(f"You have written {lines} lines({chars} characters) across {files} \
files for GameGui, and that's about {chars//3000} headaches.")
