
from pygame import draw


class Render(object):

    def __init__(self, window, world):
        self.window = window
        self.world = world


    def draw_world(self):
        self.window.display_surface.fill((0, 0, 0))
        for item in self.world.items:
            self.draw_platform(item)


    def draw_platform(self, item):
        draw.polygon(
            self.window.display_surface,
            (255, 0, 0),
            item.verts, 0)

