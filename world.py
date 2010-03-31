
from math import pi
from random import randint, uniform

from pymunk import init_pymunk, Space

from items import Ground, Branch, Bough, Woger


def populate(world):
    ground = Ground()
    world.add_item(ground)

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

    def in_air(space, arbiter, woger):
        woger.in_air = True
        return 1

    def landed(space, arbiter, woger):
        woger.in_air = False
        return 1    
    
    world.add_collision_handler(ground, woger, begin=landed, separate=in_air, woger=woger)
    


class World(object):

    def __init__(self):
        self.items = []
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -0.1)
        self.space.resize_static_hash()
        self.space.resize_active_hash()


    def add_item(self, item):
        self.items.append(item)
        item.create_body()
        item.add_to_space(self.space)

    def update(self):
        self.space.step(1)

    def add_collision_handler(self, obj1, obj2,
                              begin=None, pre_solve=None,
                              post_solve=None, separate=None,
                              **kwargs):
        self.space.add_collision_handler(obj1.shape.collision_type,
                                         obj2.shape.collision_type,
                                         begin, pre_solve,
                                         post_solve, separate,
                                         **kwargs)