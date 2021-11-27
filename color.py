from operator import mul as _mul
from functools import partial
from itertools import zip_longest
name_color_map = {
"red":(255,0,0),
"green":(0,255,0),
"blue":(0,0,255),
"yellow":(255,255,0),
"purple":(255,0,255),
"aqua":(0,255,255),
"black":(0,0,0),
"white":(255,255,255),
"lightblue":(100,100,255),
"gray":(160,160,160)}
def solid(color):
    return color[:3]
def alpha(color):
    return color[3] if len(color)==4 else 255
def name2color(name):
    return name_color_map[name.lower().strip()]
def apply(color,func):
    return tuple(map(func,color))
def saturate(color,sat):
    func = partial(_mul,sat)
    return apply(color,func)
def clampi(x):
    return max(0,min(255,x))
def clamp(color):
    return apply(color,clampi)
def displaycolor(color):
    return apply(clamp(color),int)
def numadd(x):
    return x[0]+x[1]
def add(a,b):
    return tuple(map(numadd,zip_longest(a,b,fillvalue=255)))
def add_amul(a,b):
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2],max(alpha(a),alpha(b)))
def grayscale(brightness):
    return (brightness,brightness,brightness)
def mix(a,b,r):
    return add(apply(a,partial(_mul,r)),apply(b,partial(_mul,1-r)))
def blend(front,back):
    alp = alpha(front)
    return mix(solid(front),solid(back)*alpha(back),alp/255)
