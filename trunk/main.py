
from __future__ import division

from pygame import display, event
from pygame.locals import QUIT, K_ESCAPE

from pymunk import DampedSpring

from window import Window
from world import World
from items import Platform
from render import Render


def main():
    window = Window()
    window.init()

    world = World()

    p1 = Platform(window.width / 2, 100)
    p2 = Platform(window.width / 2, 500)
    world.add(p1)
    world.add(p2)

    spring = DampedSpring(p1.body, p2.body, (0, 100), (100, 100), 40, 100, 10)
    world.space.add(spring)
    p1.body.apply_impulse((0, 0), (500000, 50000))

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

