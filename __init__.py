"""\
A library for easy widgets in python pygame."""
import pygame
pygame.init()
from . import disp
from .disp.winmgr import place as display_at,Window
from .events import *
from .widgets import *
