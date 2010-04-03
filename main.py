
from __future__ import division

import sys
import subprocess

import pygame
from pygame.locals import *

from pygame import display, event

import random

##from pygame.locals import (
##    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_RETURN, KMOD_ALT,
##    K_LEFT, K_RIGHT, K_SPACE,
##)

from window import Window
from world import World, populate
from render import Render
from sounds import Sounds

from intro import main as intro_main

CLEANUP = USEREVENT + 1
TICK_TOCK = USEREVENT + 2
ADDCHERRY = USEREVENT + 3
ADDOWANGE = USEREVENT + 4

def start_game():

    #needs to be called before pygame.init
    pygame.mixer.pre_init(22050, -16, 2, 1024)

    window = Window()
    window.init()

    pygame.init()

##    intro_main(window)
##    import sys
##    sys.exit()
    
    sounds = Sounds()
    sounds.init()

    # so we can mix more channels at once.  pygame defaults to 8.
    pygame.mixer.set_num_channels(32)
    sounds.play("jump1")
    sounds.play("hit1")
    sounds.play("goal1")
    #sounds.play_music("track-one")
    sounds.music_tracks(['track-one', 'track-two'])

    world = World()
    populate(world, window)

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

    AddCherry = pygame.event.Event(ADDCHERRY, message="Ooooo Cherry")
    pygame.time.set_timer(ADDCHERRY, 90000/5)
       
    AddOwange = pygame.event.Event(ADDOWANGE, message="Ooooo owange")
    pygame.time.set_timer(ADDOWANGE, 1000 * 5)
       



    render = Render(window, world)
    runloop(window, world, render)

 

def runloop(window, world, render):


    clock = pygame.time.Clock()
    clock.tick()
    FPS = 30
    
    while True:
        clock.tick(FPS)
        #TODO: hacky hack.  This is not very accurate, will do for now.
        elapsed_time = 1./FPS

        if handle_events(window, world):
            break
        Sounds.sounds.update(elapsed_time)
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

        if e.type == ADDCHERRY:
            print "Adding cherry"
            bounds = window.width
            world.add_cherry(random.randint(-bounds, bounds), window.height-200)

        if e.type == ADDOWANGE:
            bounds = window.width
            world.add_owange(random.randint(-bounds/2, bounds/2), window.height)


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
##            elif woger.allowed_glide or not woger.in_air:
            else:
                if e.key == K_LEFT:
                    woger.do_walk(-1)
                elif e.key == K_RIGHT:
                    woger.do_walk(1)
     
                elif (e.key == K_SPACE or e.key == K_UP) and (woger.allowed_jump or not woger.in_air):
                    woger.jump()

                elif e.key == K_DOWN and not woger.in_air:
                    woger.dive()

            if 1 and e.key == K_s and e.mod & KMOD_SHIFT:
                pygame.image.save( pygame.display.get_surface() , "screeny.png")


##        elif woger.allowed_glide or not woger.in_air:
        else:
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

