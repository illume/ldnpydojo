from __future__ import division

import os
from pygame import display, event, font
from pygame.locals import QUIT, K_ESCAPE
from pymunk import Vec2d

##from window import Window
from .world import World
from .items import Platform, Spring, Word
from render import Render
from ..data import data_dir

        
def main(window, handle_events, score):
##    window = Window()
##    window.init()

    world = World()
    world.stage = 3

    p1 = Platform(600, 300, 400, 50)
    world.add_item(p1)
    p2 = Platform(500, 600, 800, 100)
    world.add_item(p2)
    
    """   vert order:
             0 3
             1 2
    """
    rest_length, stiffness, damping = 200, 10, 1
    spring = Spring(p1, p2,
                    lambda vs:vs[1],
                    lambda vs:vs[0],
                    rest_length, stiffness, damping)
    world.add_spring(spring)

    spring = Spring(p1, p2,
                    lambda vs:vs[2],
                    lambda vs:vs[3],
                    rest_length, stiffness, damping)
    world.add_spring(spring)

    spring = Spring(p1, p2,
                    lambda vs: (vs[1] + vs[3])/2,
                    lambda vs: (vs[1] + vs[3])/2,
                    rest_length, 10*stiffness, damping)
    world.add_spring(spring)

    
    font_path = os.path.join(data_dir(), "fonts", "vinque", "vinque.ttf")

##    fnt = font.Font(font_path, 36)
##    surface = fnt.render('The adventures of...', True, (255,255,255))
##    word = Word(p2, surface, (200, 50))
##    world.add_word(word)


    fnt = font.Font(font_path, 48)
    text = 'You scored'
    words = [fnt.render(word, True, (0,0,0))
                     for word in text.split()]

    word_positions = (
        (150, 60),
        (550, 60),
        )

    for surface, position in zip(words, word_positions):
        word = Word(p1, surface, position)
        world.add_word(word)

    fnt = font.Font(font_path, 96)
    surface = fnt.render('% 2d' %score, True, (255,255,255))
    word = Word(p2, surface, (230, 350))
    world.add_word(word)

    fnt = font.Font(font_path, 24)
    surface = fnt.render('space to play again, escape to quit', True, (0,0,0))
    word = Word(p2, surface, (200, 550))
    world.add_word(word)
    
    render = Render(window, world)

    while True:
        quit = handle_events(window, world)
        if quit == 2:
            # non-esc keypressed
            return False
        if quit:
            return quit

        world.update()
        render.draw_world()
        display.flip()



##def handle_events():
##    for e in event.get():
##        if e.type == QUIT or getattr(e, 'key', None) == K_ESCAPE:
##            return True


##if __name__ == '__main__':
##    try:
##        main()
##    finally:
##        pass
##        #display.quit()

