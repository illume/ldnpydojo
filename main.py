from __future__ import division

from pygame import display, event
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, KMOD_ALT

from window import Window
from world import World
from items import Platform, Spring, Woger
from render import Render



def populate(world):

    p1 = Platform(600, 300, 400, 50)
    world.add_item(p1)
    p2 = Platform(500, 600, 800, 100, static=True)
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

    world.add_item(Woger(300, 000))

        
def main():
    window = Window()
    window.init()

    world = World()
    populate(world)

    render = Render(window, world)

    while True:
        if handle_events(window):
            break

        world.update()
        render.draw_world()
        display.flip()



def handle_events(window):
    quit = False
    for e in event.get():
        if e.type == QUIT or getattr(e, 'key', None) == K_ESCAPE:
            quit = True
            break
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit = True
                break
            elif e.key == K_RETURN and e.mod & KMOD_ALT:
                window.toggle_fullscreen()
    return quit


if __name__ == '__main__':
    try:
        main()
    finally:
        display.quit()

