
from pygame import draw

from items import Platform


class Render(object):

    def __init__(self, window, world):
        self.window = window
        self.world = world


    def draw_world(self):
        self.window.display_surface.fill((0, 0, 0))
        for item in self.world.items:
            self.draw_platform(item)
        for spring in self.world.springs:
            self.draw_spring(spring)
        

    def draw_spring(self, spring):
        draw.line(
            self.window.display_surface,
            (80, 120, 90),
            spring.verts_to_anchor1(spring.p1.verts),
            spring.verts_to_anchor2(spring.p2.verts),
            15)

    def draw_platform(self, item):
        draw.polygon(
            self.window.display_surface,
            (255, 0, 0),
            item.verts, 0)

