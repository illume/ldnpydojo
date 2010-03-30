
from pygame import draw



class Camera(object):

    def __init__(self, window):
        self.window = window

    def to_screen(self, verts):
        return [(x + self.window.width / 2, self.window.height - 100 - y)
                for (x, y) in verts]



class Render(object):

    def __init__(self, window, world):
        self.window = window
        self.world = world
        self.camera = Camera(window)


    def draw_world(self):
        self.window.display_surface.fill((0, 100, 255))
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
            item.color,
            self.camera.to_screen(item.verts), 0)

