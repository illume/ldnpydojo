from __future__ import division

from pygame import display, event
from pygame.locals import QUIT, K_ESCAPE
from pymunk import Vec2d

from window import Window
from world import World
from items import Platform, Spring
from render import Render



        
def main():
    window = Window()
    window.init()

    world = World()

    p1 = Platform(600, 100, 400, 50)
    world.add(p1)
    p2 = Platform(300, 500, 800, 100)
    world.add(p2)

# vert order:
#    0 3
#    1 2
    spring = Spring(p1, p2,
                    offset1=Vec2d(p1.verts[2])-Vec2d(p1.centre),
                    offset2=Vec2d(p2.verts[3])-Vec2d(p2.centre),
                    verts_to_anchor1=lambda vs:vs[2],
                    verts_to_anchor2=lambda vs:vs[3],
                    rest_length=500, stiffness=100, damping=100)
    world.add_spring(spring)

    spring = Spring(p1, p2,
                    offset1=Vec2d(p1.verts[2])-Vec2d(p1.centre),
                    offset2=Vec2d(p2.verts[3])-Vec2d(p2.centre),
                    verts_to_anchor1=lambda vs:vs[2],
                    verts_to_anchor2=lambda vs:vs[3],
                    rest_length=500, stiffness=100, damping=100)
    world.add_spring(spring)

    spring = Spring(p1, p2,
                    offset1=(0, 0),
                    offset2=(0, 0),
                    verts_to_anchor1=lambda vs: (vs[1] + vs[3])/2,
                    verts_to_anchor2=lambda vs: (vs[1] + vs[3])/2,
                    rest_length=500, stiffness=1000, damping=100)
    world.add_spring(spring)   
    

    
##    sensible = 1
##    if sensible:
##        p1.body.apply_impulse((0, +5000), (-100, 0))
##    else:
##        p1.body.apply_impulse((+280000, 10000), (-100, 0))
##        p2.body.apply_impulse((-280000, -000), (-100, 0))

    render = Render(window, world)

    while True:
        quit = handle_events()
        if quit:
            break

        world.update()
        render.draw_world()
        display.flip()



def handle_events():
    for e in event.get():
        if e.type == QUIT or getattr(e, 'key', None) == K_ESCAPE:
            return True


if __name__ == '__main__':
    try:
        main()
    finally:
        display.quit()

