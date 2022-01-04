from .bases import Widget
class CustomWidget(Widget):
    """Custom widget support.
size: a 2-tuple (width,height) of the dimensions of this widget.
constructor: a function taking the blank surface for input and \
draws on the surface. If the function does not return None, the return \
value is considered to be the surface. If the function returns None,
then it is considered to be an in-place operation."""
    def __init__(self,size,constructor,fill=(0,0,0,0)):
        self.width,self.height = size
        self.constructor = constructor
        self.fill = fill
    def get_surface(self):
        surface = self.blank()
        surface.fill(self.fill)
        rslt = self.constructor(surface)
        if rslt is not None:
            surface = rslt
        return surface
