
from __future__ import division

import sys
from math import pi
from random import uniform, randint
import subprocess

from pygame import display, event
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, KMOD_ALT

from window import Window
from world import World, populate
from render import Render



def start_game():
    window = Window()
    window.init()
    world = World()
    populate(world)
    render = Render(window, world)
    runloop(window, world, render)


def runloop(window, world, render):
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
    command = 'start_game()'
    filename = 'pyweek10-ldnpydojo.profile'
    cProfile.runctx( command, globals(), locals(), filename=filename )
    subprocess.call( ['runsnake', filename] )


def main():
    try:
        if '--profile' in sys.argv:
            profile()
        else:
            start_game()
    finally:
        display.quit()


if __name__ == '__main__':
    main()

