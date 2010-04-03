
from math import pi
from random import randint, uniform

from pymunk import init_pymunk, Space

from items import BoundingTrunk, CollisionType, Ground, Branch, Bough, Woger, Owange

from sounds import Sounds

from pygame import time

import random


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

    trunk = add_branch(ground, 0, 50, 250)

    woger = Woger(200, 450)
    world.add_item(woger)
    world.player_character = woger


    def landed_on_ground(space, arbiter, woger):
        woger.in_air = False
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
    def off_leaf(space, arbiter, woger):
        woger.in_air = True
        Sounds.sounds.play("hit1")
        return 1    


    def touch_owange(space, arbiter, woger):
        ''' when woger hits an owange.
        '''
        owanges = [s.parent for s in arbiter.shapes 
                      if hasattr(s, 'parent') and isinstance(s.parent, Owange)]

        for o in owanges:
            if o.status == "Collided":
                pass
            else:
                woger.score += 1
                Sounds.sounds.play("powerup1")
                world.remove_item(o)
                # add owange from the top again.
                owange = Owange(randint(0, bounds), 750) 
                world.add_item(owange)

                    

        return 1
    def off_owange(space, arbiter, woger):
        return 1    



    def owange_hit_ground(space, arbiter, woger):

        owanges = [s.parent for s in arbiter.shapes 
                      if hasattr(s, 'parent') and isinstance(s.parent, Owange)]

        for o in owanges:
            Sounds.sounds.play("orange_splat")
            o.destroy()
            #o.status = "Collided"
            #world.remove_item(o)
            # add owange from the top again.
            owange = Owange(randint(0, bounds), 750) 
            world.add_item(owange)

        return 1

    def owange_off_ground(space, arbiter, woger):
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
                                separate=off_leaf, woger=woger)
    
    world.add_collision_handler(CollisionType.OWANGE, CollisionType.PLAYER,
                                begin=touch_owange, 
                                separate=off_owange, woger=woger)
    
    world.add_collision_handler(CollisionType.GROUND, CollisionType.OWANGE,
                                begin=owange_hit_ground, 
                                separate=owange_off_ground, woger=woger)


class World(object):

    def __init__(self):
        self.items = []
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -0.5)
        self.space.resize_static_hash()
        self.space.resize_active_hash()
        self.leaves = []
        


    def add_item(self, item):
        if isinstance(item, Bough):
            self.leaves.append(item)
        self.items.append(item)
        item.create_body()
        item.add_to_space(self.space)

    def remove_item(self, item):
        self.items.remove(item)
        item.remove_from_space(self.space)


    def update(self):
        self.space.step(0.5)
        for item in self.items:
            item.update()

    def remove_collided(self):
        for item in self.items:
            if item.status == "Collided":
                self.remove_item(item)
            
    def tick(self):
        print "Off comes a leaf"
        max_limit = len(self.leaves) - 1
        if len(self.leaves) == 0:
                max_limit = 0 
                print "End Level"
                pass

        else:
            print max_limit
            randno = random.randint(0, max_limit)
            print randno
            leaf = self.leaves.pop(randno)
            print leaf
            leaf.remove_from_tree(self.space)

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

