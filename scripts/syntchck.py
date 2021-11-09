import os,traceback,sys
def ep(*a,**k):
    print(*a,file=sys.stderr,**k)
syntfail = False
for curr,subd,subf in os.walk(".."):
    for f in subf:
        if f.endswith(".py") or f.endswith(".pyw"):
            try:
                ctx = open(os.path.join(curr,f)).read()
            except:
                ep(f"--ERROR OPENING: {os.path.join(curr,f)}--")
                traceback.print_exc()
            else:
                try:
                    compile(ctx,os.path.join(curr,f),"exec")
                except SyntaxError:
                    ep(f"--CHECK FAILED FOR: {os.path.join(curr,f)}--")
                    traceback.print_exc()
                    syntfail = True
if syntfail:
    os._exit(-1)#fail
