from __future__ import division

from pygame import display, event
from pygame.locals import QUIT, K_ESCAPE
from pymunk import Vec2d

from window import Window
from world import World
from items import Platform, Spring
from render import Render


        
def main():
    window = Window()
    window.init()

    world = World()

    p1 = Platform(600, 300, 400, 50)
    world.add_item(p1)
    p2 = Platform(500, 600, 800, 100)
    world.add_item(p2)
    
    """   vert order:
             0 3
             1 2
    """
    spring = Spring(p1, p2,
                    lambda vs:vs[1],
                    lambda vs:vs[0],
                    200, 10, 1)
    world.add_spring(spring)

    spring = Spring(p1, p2,
                    lambda vs:vs[2],
                    lambda vs:vs[3],
                    200, 10, 1)
    world.add_spring(spring)

    spring = Spring(p1, p2,
                    lambda vs: (vs[1] + vs[3])/2,
                    lambda vs: (vs[1] + vs[3])/2,
                    200, 100, 1)
    world.add_spring(spring)

    
##    p1.body.apply_impulse((0, +5000), (-100, 0))

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
    try:
        main()
    finally:
        display.quit()

