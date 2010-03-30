from __future__ import division

from math import pi

from pygame import display, event
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, KMOD_ALT

from window import Window
from world import World
from items import Branch, Ground, Woger
from render import Render



def populate(window, world):
    ground = Ground()
    world.add_item(ground)

    def add_branch(parent, angle, thickness, length):
        branch = Branch(parent, angle, thickness, length)
        world.add_item(branch)
        if thickness > 30:
            newthickness = thickness * 0.75
            newlength = length * 0.75
            for i in xrange(5):
                newangle = angle - pi/2 + i * pi/4
                add_branch(
                    branch,
                    newangle,
                    newthickness,
                    newlength)
        return branch

    trunk = add_branch(ground, 0, 50, 400)
    trunk.body.apply_impulse((100000, 0), (0, 500))

    woger = Woger(600, 100)
    world.add_item(woger)

        
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

