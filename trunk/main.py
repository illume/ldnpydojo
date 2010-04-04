
from __future__ import division

import sys,os
import subprocess
import glob

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
from outro import main as outro_main

CLEANUP = USEREVENT + 1
TICK_TOCK = USEREVENT + 2
ADDCHERRY = USEREVENT + 3
ADDOWANGE = USEREVENT + 4
BIRDY = USEREVENT + 5

def start_game():

    #needs to be called before pygame.init
    pygame.mixer.pre_init(22050, -16, 2, 1024)

    window = Window()
    window.init()

    pygame.init()

    sounds = Sounds()
    sounds.init()
    window.sounds = sounds
    pygame.mixer.set_num_channels(32)

    # meta game loop    
    while True:
        sounds.play_music("intro", loop=1)
        intro_main(window, handle_events)
        

        # so we can mix more channels at once.  pygame defaults to 8.
        #sounds.play("jump1")
        #sounds.play("hit1")
        #sounds.play("goal1")
        sounds.set_music_tracks(['track-one', 'track-two'])

        world = World()
        world.stage = 2
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

        for i in range(3):
            event.post(AddOwange)        
           
        pygame.time.set_timer(BIRDY, 1000 * 7)



        render = Render(window, world)
        quit = runloop(window, world, render)
        if quit:
            return 
    

 

def runloop(window, world, render):


    clock = pygame.time.Clock()
    clock.tick()
    FPS = 30
    
    while True:
        clock.tick(FPS)
        #TODO: hacky hack.  This is not very accurate, will do for now.
        elapsed_time = 1./FPS

        if handle_events(window, world):
            # show score outro
            break
##            return True
        Sounds.sounds.update(elapsed_time)
        world.update()
        render.draw_world()
        display.flip()
        if world.end_game:
            break

    #show score
        
    window.sounds.play_music("intro", loop=1)
    quit = outro_main(window, handle_events, world.player_character.score)
    return quit



def handle_events(window, world):
    quit = False
    for e in event.get():

        if e.type == QUIT:
            quit = True
            break     

        elif e.type == KEYDOWN:
            if 1 and e.key == K_s and e.mod & KMOD_SHIFT:
                pygame.image.save( pygame.display.get_surface() , "screeny.png")
                
            if e.key == K_ESCAPE:
                quit = True
                break
            elif e.key == K_RETURN and e.mod & KMOD_ALT:
                window.toggle_fullscreen()
        
            if world.stage == 1:
                #any key quits the intro
                quit = True
                return quit
            
            elif world.stage == 3:
                # anykey replays game, esc quits
                if quit:
                    return quit
                else:
                    # non-esc keypressed
                    return 2
        
            # Woger
##            elif woger.allowed_glide or not woger.in_air:
            woger = world.player_character
            if e.key == K_LEFT:
                woger.do_walk(-1)
            elif e.key == K_RIGHT:
                woger.do_walk(1)
 
            elif (e.key == K_SPACE or e.key == K_UP) and not woger.in_air:
                woger.jump()

            elif e.key == K_DOWN and not woger.in_air:
                woger.dive()
        
        elif world.stage in (1, 3):
            # no key down, but stop here, we're in intro/outro
            return quit
            
##        elif woger.allowed_glide or not woger.in_air:
        elif e.type == KEYUP:
            woger = world.player_character
            if e.key == K_LEFT:
                woger.end_walk()
            elif e.key == K_RIGHT:
                woger.end_walk()


        elif e.type == CLEANUP:
            world.remove_collided()

        elif e.type == TICK_TOCK:
            world.tick()

        elif e.type == ADDCHERRY:
            bounds = window.width
            world.add_cherry(random.randint(-bounds/2, bounds/2), 
                            random.randint(window.height-300,window.height ))

        elif e.type == ADDOWANGE:
            bounds = window.width
            world.add_owange(random.randint(-bounds/2, bounds/2), 
                            random.randint(window.height-300,window.height ))

        elif e.type == BIRDY:
            bird_files = glob.glob(os.path.join('data','sounds','birds*.ogg'))
            bsounds = [os.path.basename(b[:-4]) for b in bird_files]
            the_sound = random.choice(bsounds)
            Sounds.sounds.play(the_sound)            

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

