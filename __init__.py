"""\
A library for easy widgets in python pygame."""
import pygame
pygame.init()
from . import color
from .disp.winmgr import *
from .events import *
from .widgets import *
from ._utils import getdeffont,setdeffont,getsysfont as SysFont,getfont as Font
from .transform import *
