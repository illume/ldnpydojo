
from pygame import display
from pygame.locals import HWSURFACE, DOUBLEBUF, FULLSCREEN



class Window(object):

    def init(self):
        display.init()
        modes = display.list_modes()
        self.display_surface = display.set_mode(modes[0],
            HWSURFACE | DOUBLEBUF | FULLSCREEN)

    @property
    def width(self):
        return self.display_surface.get_width()

