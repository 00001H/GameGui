from .custom import CustomWidget
import pygame
class Image:
    """Simple image class.
Constructor: Image([file,[alpha]])

file is the file to load, if none, creates a 0x0 empty image.
alpha decides if the per-pixel alpha channel should be kept when loading the image.
"""
    def __init__(self,file=None,alpha=True):
        self.file = file
        self.has_alpha = alpha
        if file:
            self.reload()
        else:
            self.surface = pygame.Surface((0,0))
            if alpha:
                self.surface = self.surface.convert_alpha()
    def reload(self):
        """Reloads the image from the file.
Raises ValueError if file is not set."""
        if self.file is None:
            raise ValueError("No file to load!")
        self.surface = pygame.image.load(self.file)
        if self.has_alpha:
            self.surface = self.surface.convert_alpha()
    def setfile(self,file,reload=True):
        """Modifies the file of the image.
reload: Whether to reload the image or keep the surface as-is."""
        self.file = file
        if reload:
            self.reload()
    def as_widget(self):
        """Converts the image to a widget(see gamegui.custom.CustomWidget for details) \
for rendering.
The returned widget has the same dimensions as the image."""
        def func(surf):
            surf.blit((0,0),self.surface)
        return CustomWidget(self.surface.get_size(),func)
