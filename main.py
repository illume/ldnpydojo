
from __future__ import division

from pygame import display, draw, event
from pygame.locals import *

from pymunk import Space, Body, Poly, moment_for_poly


class Window(object):

    def init(self):
        display.init()
        modes = display.list_modes()
        self.display_surface = display.set_mode(modes[0],
            HWSURFACE | DOUBLEBUF | FULLSCREEN)

    @property
    def width(self):
        return self.display_surface.get_width()


class World(object):

    def __init__(self):
        self.items = []
        self.space = Space()

    def add(self, item):
        self.items.append(item)
        self.space.add(item.shape)
        self.space.add(item.body)

    def update(self):
        self.space.step(1)



class Platform(object):

    def __init__(self, x, y, angle=0.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.width = 400
        self.height = 50

        verts = (
            (self.x - self.width / 2, self.y - self.height / 2),
            (self.x - self.width / 2, self.y + self.height / 2),
            (self.x + self.width / 2, self.y + self.height / 2),
            (self.x + self.width / 2, self.y - self.height / 2),
        )
        self.mass = self.width * self.height
        self.body = Body(
            self.mass, moment_for_poly(self.mass, verts))
        self.shape = Poly(self.body, verts, (0, 0))
        self.body.apply_impulse((0, 100000), (500, 50))


    @property
    def verts(self):
        return self.shape.get_points()



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


def main():
    window = Window()
    window.init()

    world = World()
    world.add(Platform(window.width / 2, 100))

    render = Render(window, world)

    while True:
        quit = handle_events()
        if quit:
            break

        world.update()

        render.draw_world()
        display.flip()



def handle_events():
    for e in event.get():
        if e.type == QUIT or getattr(e, 'key', None) == K_ESCAPE:
            return True


if __name__ == '__main__':
    main()

