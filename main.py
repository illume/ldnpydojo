
from __future__ import division

import sys
import subprocess

import pygame
from pygame.locals import *

from pygame import display, event

##from pygame.locals import (
##    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_RETURN, KMOD_ALT,
##    K_LEFT, K_RIGHT, K_SPACE,
##)

from window import Window
from world import World, populate
from render import Render
from sounds import Sounds

CLEANUP = USEREVENT + 1
TICK_TOCK = USEREVENT + 2

def start_game():

    window = Window()
    window.init()
    pygame.init()
    sounds = Sounds()
    sounds.init()
    sounds.play("jump1")
    sounds.play("hit1")
    sounds.play("goal1")
    sounds.play_music("track-one")

    world = World()
    populate(world)

    def count_leaves():
        no_leaves = 0
        for item in world.items:
            if item.role == "Bough":
                no_leaves = no_leaves + 1
        return no_leaves
    
    CleanUp_Event = pygame.event.Event(CLEANUP, message="Cleaning Up Your shit")
    pygame.time.set_timer(CLEANUP, 1000)
    TickTock = pygame.event.Event(TICK_TOCK, message="TickTock goes the Ticking Clock")
    pygame.time.set_timer(TICK_TOCK, 90000/count_leaves())

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
        print e

        if e.type == CLEANUP:
            #print "Cleaning"
            world.remove_collided()

        if e.type == TICK_TOCK:
            world.tick()
            
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
            elif woger.allowed_glide or not woger.in_air:
                if e.key == K_LEFT:
                    woger.do_walk(-1)
                elif e.key == K_RIGHT:
                    woger.do_walk(1)
     
                elif e.key == K_SPACE and (woger.allowed_jump or not woger.in_air):
                    woger.jump()

            if 1 and e.key == K_s and e.mod & KMOD_SHIFT:
                pygame.image.save( pygame.display.get_surface() , "screeny.png")


        elif woger.allowed_glide or not woger.in_air:   
            if e.type == KEYUP:
                if e.key == K_LEFT:
                    woger.end_walk()
                elif e.key == K_RIGHT:
                    woger.end_walk()



    if woger.walk_force:
        woger.do_walk()

    return quit


def profile(command):
    import cProfile
    filename = 'pyweek10-ldnpydojo.profile'
    cProfile.runctx( command, globals(), locals(), filename=filename )
    subprocess.call( ['runsnake', filename] )


def main():
    try:
        if '--profile' in sys.argv:
            profile('start_game()')
        else:
            start_game()
    finally:
        display.quit()


if __name__ == '__main__':
    main()

