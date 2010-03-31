
from __future__ import division

import sys
from math import pi
from random import uniform, randint
import subprocess

from pygame import display, event
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, KMOD_ALT

from window import Window
from world import World
from items import Branch, Bough, Ground, Woger
from render import Render



def populate(window, world):
    ground = Ground()
    world.add_item(ground)

    def add_branch(parent, angle, thickness, length):
        branch = Branch(parent, angle, thickness, length)
        world.add_item(branch)

        bough = Bough(branch)
        world.add_item(bough)

        if thickness > 25:
            branches = randint(3, 4)
            spread = uniform(pi / 8, pi / branches)
            for i in xrange(branches):
                delta_angle = spread * (branches - 1) / 2 - spread * i
                newangle = angle + delta_angle
                newlength = length * (1 - abs(delta_angle) / 2.5)
                newthickness = thickness * 0.75
                add_branch(
                    branch,
                    newangle,
                    newthickness,
                    newlength)
        return branch

    trunk = add_branch(ground, 0, 50, 400)

    woger = Woger(200, 1000)
    world.add_item(woger)


def runloop():
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


def profile():
    import cProfile
    command = 'runloop()'
    filename = 'pyweek10-ldnpydojo.profile'
    cProfile.runctx( command, globals(), locals(), filename=filename )
    subprocess.call( ['runsnake', filename] )


def main():
    try:
        if '--profile' in sys.argv:
            profile()
        else:
            runloop()
    finally:
        display.quit()


if __name__ == '__main__':
    main()

