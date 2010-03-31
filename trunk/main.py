
from __future__ import division

import sys
import subprocess

from pygame import display, event
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_RETURN, KMOD_ALT, K_LEFT, K_RIGHT, K_SPACE

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
        if handle_events(window, world):
            break

        world.update()
        render.draw_world()
        display.flip()


def handle_events(window, world):
    woger = world.player_character
    quit = False
    for e in event.get():
        if e.type == QUIT:
            quit = True
            break
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit = True
                break
            elif e.key == K_RETURN and e.mod & KMOD_ALT:
                window.toggle_fullscreen()

            # Woger
            elif e.key == K_LEFT:
                woger.do_walk(-1)
            elif e.key == K_RIGHT:
                woger.do_walk(1)

            elif e.key == K_SPACE
                
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                woger.end_walk()
            elif e.key == K_RIGHT:
                woger.end_walk()

            
                
    if woger.walk_force:
        woger.cont_walk()
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

