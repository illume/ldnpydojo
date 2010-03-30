from __future__ import division

from pygame import display, event, Rect
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, KMOD_ALT
from pymunk import Vec2d

from window import Window
from world import World
from items import Platform, Spring, Woger
from render import Render



def populate(window, world):
    base_size = Vec2d(2000, 100)
    base_centre = (base_size[0]/2, window.height-60)
    
    base_topleft = Vec2d(base_centre - base_size/2)
    base = Platform(*Rect(base_centre, base_size), static=True)
    world.add_item(base)

    platform = Platform(600, window.height-300, 400, 50)
    world.add_item(platform)    
    
    """   vert order:
             0 3
             1 2
    """
    spring = Spring(base, platform,
                    lambda _:base_topleft,
                    lambda vs:vs[1],
                    200, 10, 1)
    world.add_spring(spring)

    spring = Spring(base, platform,
                    lambda _:base_topleft+(1600, 0),
                    lambda vs:vs[2],
                    200, 10, 1)
    world.add_spring(spring)

    spring = Spring(base, platform,
                    lambda v_:base_topleft+(800, 0),
                    lambda vs: (vs[1] + vs[3])/2,
                    400, 100, 1)
    world.add_spring(spring)

    world.add_item(Woger(300, 000))

        
def main():
    window = Window()
    window.init()

    world = World()
    populate(window, world)

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

