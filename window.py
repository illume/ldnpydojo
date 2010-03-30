
from pygame import display
from pygame.locals import HWSURFACE, DOUBLEBUF, FULLSCREEN


FLAGS = HWSURFACE | DOUBLEBUF


class Window(object):

    def init(self):
        self.fullscreen = False
        display.init()
        self.set_mode()


    def set_mode(self):
        modes = display.list_modes()
        self.display_surface = display.set_mode(modes[0], self.get_flags())


    def get_flags(self):
        return FLAGS if not self.fullscreen else FLAGS | FULLSCREEN


    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.set_mode()


    @property
    def width(self):
        return self.display_surface.get_width()

