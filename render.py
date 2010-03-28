
from pygame import draw


class Render(object):

    def __init__(self, window, world):
        self.window = window
        self.world = world


    def draw_world(self):
        self.window.display_surface.fill((0, 0, 0))
        for item in self.world.items:
            self.draw_platform(item)
        self.draw_spring()

    def draw_spring(self):
        p1, p2 = self.world.items
        draw.line(self.window.display_surface, (80, 120, 90), p1.centre, p2.centre, 15)


    def draw_platform(self, item):
        draw.polygon(
            self.window.display_surface,
            (255, 0, 0),
            item.verts, 0)

