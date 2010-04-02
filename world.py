
from math import pi
from random import randint, uniform

from pymunk import init_pymunk, Space

from items import BoundingTrunk, CollisionType, Ground, Branch, Bough, Woger, Owange

from sounds import Sounds


def populate(world):
    ground = Ground()
    world.add_item(ground)

    bounds = 500
    world.add_item(BoundingTrunk(-bounds))
    world.add_item(BoundingTrunk(+bounds))

    def add_branch(parent, angle, thickness, length):
        branch = Branch(parent, angle, thickness, length)
        world.add_item(branch)

        if thickness < 25:
            bough = Bough(branch)
            world.add_item(bough)
        else:
            branches = randint(3, 4)
            spread = uniform(pi / 8, pi / branches)
            for i in xrange(branches):
                delta_angle = spread * (branches - 1) / 2 - spread * i
                newangle = angle + delta_angle
                newlength = length * (1 - abs(delta_angle) / 2.5)
                newthickness = thickness * 0.75
                add_branch( branch, newangle, newthickness, newlength )
        return branch

    trunk = add_branch(ground, 0, 50, 300)

    woger = Woger(200, 450)
    world.add_item(woger)
    world.player_character = woger


    def landed_on_ground(space, arbiter, woger):
        woger.in_air = True
        woger.allowed_glide = 2
        woger.allowed_jump = 1
        return 1
    
    def off_ground(space, arbiter, woger):
        woger.in_air = False
        Sounds.sounds.play("hit1")
        return 1    


    def touch_leaf(space, arbiter, woger):
        woger.in_air = True
        woger.allowed_glide = 2
        woger.allowed_jump = 1
        return 1
    
    def leave_leaf(space, arbiter, woger):
        woger.in_air = False
        Sounds.sounds.play("hit1")
        return 1    


    def touch_owange(space, arbiter, woger):
        # 
        owanges = [s.parent for s in arbiter.shapes 
                      if hasattr(s, 'parent') and isinstance(s.parent, Owange)]

        for o in owanges:
            Sounds.sounds.play("powerup1")
            world.remove_item(o)
            # add owange from the top again.
            owange = Owange(randint(0, bounds), 750) 
            world.add_item(owange)

        return 1
 
    def leave_owange(space, arbiter, woger):
        return 1    

   



    #TODO: owanges will need to be dropped as the game goes on.
    #  when colliding with woger points are scored.
    #  when colliding with the ground, 
    #      points are lost
    #      owanges go splat
    #      owanges dissapear

    for i in range(10):
        owange = Owange(i*10, 650) 
        world.add_item(owange)
        #world.remove_item(owange)

    
        

    world.add_collision_handler(CollisionType.GROUND, CollisionType.PLAYER,
                                begin=landed_on_ground, 
                                separate=off_ground, woger=woger)
    world.add_collision_handler(CollisionType.BOUGH, CollisionType.PLAYER,
                                begin=touch_leaf, 
                                separate=leave_leaf, woger=woger)
    world.add_collision_handler(CollisionType.OWANGE, CollisionType.PLAYER,
                                begin=touch_owange, 
                                separate=leave_owange, woger=woger)


class World(object):

    def __init__(self):
        self.items = []
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -0.5)
        self.space.resize_static_hash()
        self.space.resize_active_hash()


    def add_item(self, item):
        self.items.append(item)
        item.create_body()
        item.add_to_space(self.space)

    def remove_item(self, item):
        self.items.remove(item)
        item.remove_from_space(self.space)
        #TODO:


    def update(self):
        self.space.step(0.5)
        for item in self.items:
            item.update()


    def add_collision_handler( self, 
                               col_typ1, 
                               col_typ2, 
                               begin=None, 
                               pre_solve=None,
                               post_solve=None, 
                               separate=None, 
                               **kwargs
        ):
        '''
        '''
        self.space.add_collision_handler(
            col_typ1, col_typ2,
            begin, pre_solve,
            post_solve, separate,
            **kwargs)

