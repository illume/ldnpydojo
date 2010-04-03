
from __future__ import division

from math import copysign

import pygame

from pygame import event, image, key
from pymunk import (
    Body, DampedRotarySpring, PivotJoint, Poly, moment_for_poly, Vec2d,
)

from sounds import Sounds
import spritesheet

import random


class CollisionType:
    GROUND, BOUGH, PLAYER, BRANCH, OWANGE, CHERRY = range(6)

class GroupType:
    GROUND, BOUGH, PLAYER, BRANCH, OWANGE = range(5)

class LayerType:
    PLAYER, ITEMS, BACKGROUND = 1,2,4
    EVERYTHING = -1

class GameRect(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = self.width * self.height / 10000
        self.layers = LayerType.EVERYTHING # collide with everything
        self.status = None


    def get_verts(self):
        return [
            (+ self.width / 2, - self.height / 2), # right bottom
            (- self.width / 2, - self.height / 2), # left bottom
            (- self.width / 2, + self.height / 2), # left top
            (+ self.width / 2, + self.height / 2), # right top
        ]


    def create_body(self):
        verts = map(Vec2d, self.get_verts())
        self.body = Body(self.mass, moment_for_poly(self.mass, verts))
        self.body.position = (self.x, self.y)
        self.shape = Poly(self.body, verts, (0, 0))
        self.shape.layers = self.layers
        # this is so you can get to it from collision handlers.
        #     eg. arbiter.shapes[0].parent 
        self.shape.parent = self


    def update(self):
        pass


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)

    def remove_from_space(self, space):
        space.remove(self.body)
        space.remove(self.shape)

    @property
    def verts(self):
        "This is the position of the item's verts as calculated by pymunk"
        return self.shape.get_points()        




    

class Ground(GameRect):

    def __init__(self):
        GameRect.__init__(self, 0, -1000, 2000, 2000)
        self.mass = 1e100
        self.color = (0, 255, 0)
        # ground should collide with everything (3 = 1 || 2)
        self.layers = LayerType.EVERYTHING
        self.role = "Ground"
        self.status = None

    def add_to_space(self, space):
        self.shape.collision_type = CollisionType.GROUND
        space.add_static(self.shape)


class BoundingTrunk(GameRect):

    def __init__(self, x):
        self.color = (0, 100, 255)
        GameRect.__init__(self, x, 1000, 50, 2000)
        self.mass = 1e100
        self.layers = LayerType.PLAYER
        self.role = "BoundingTrunk"
        self.status = None

    def add_to_space(self, space):
        # TODO: more interesting collision to allow ninja double jumps
        self.shape.collision_type = CollisionType.GROUND
        space.add_static(self.shape)

class TopTrunk(GameRect):

    def __init__(self, y):
        self.color = (100, 100, 255)
        GameRect.__init__(self, 0, y, 2000, 50)
        self.mass = 1e100
        self.role = "BoundingTrunk"
        self.status = None
        self.layers = LayerType.PLAYER
        self.group = GroupType.BRANCH

    def add_to_space(self, space):
        # TODO: more interesting collision to allow ninja double jumps
        self.shape.collision_type = CollisionType.GROUND
        space.add_static(self.shape)
        # bough collides with ground and woger

class Branch(GameRect):
    
    def __init__(self, parent, angle, width=None, height=None, y = None):
        self.parent = parent
        self.angle = angle
        if width == None:
            width = parent.width / 2
        if height == None:
            height = parent.height / 2
 #       GameRect.__init__(self, 0, height/2, width, height)
        if y is None:
            y = height/2
        print "HEIGHT ", y
        GameRect.__init__(self, 0, y, width, height)
        self.color = (128, 64, 0)
        self.role = "Branch"
        self.status = None

        # branches should only collide with ground
        self.layers = LayerType.BACKGROUND


    def rotate_verts_about(self, verts, angle, pivot):
        return [
            (vert + pivot).rotated(angle) - pivot
            for vert in verts
        ]

    def get_verts(self):
        verts = GameRect.get_verts(self)
        tail = self.tail(verts)
        return self.rotate_verts_about(verts, self.angle, tail)

    def tip(self):
        return self.midpoint(2, 3)

    def tail(self, verts=None):
        return self.midpoint(0, 1, verts)

    def midpoint(self, v1, v2, verts=None):
        if verts is None:
            verts = self.verts
        return ( Vec2d(verts[v1]) + Vec2d(verts[v2]) ) / 2


    def create_body(self):
        verts = self.get_verts()

        self.body = Body(self.mass, moment_for_poly(self.mass, verts))
        root = Vec2d(0, 0)
        if isinstance(self.parent, Branch):
            root = self.parent.tip()
        self.body.position = root - self.tail(verts)

        self.shape = Poly(self.body, verts)

        # branch should not collide with other branches, which will
        # overlap slightly at the joints
        self.shape.group = GroupType.BRANCH

        # branches should collide only with ground
        self.shape.layers = LayerType.BACKGROUND
        self.collision_type = CollisionType.BRANCH


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)

        pivot = PivotJoint(self.body, self.parent.body, self.tail())
        space.add(pivot)

        spring = DampedRotarySpring(
            self.body, self.parent.body, 0.0, self.mass * 10000, self.mass/10)
        space.add(spring)
        


class Bough(GameRect):

    def __init__(self, branch):
        self.branch = branch
        x, y = branch.tip()
        width = branch.height
        height = width / 4
        GameRect.__init__(self, x, y, width, height)
        self.color = (0, 255, 0)
        self.role = "Bough"
        self.status = None
        #self.image = [image.load("data/art/leaves/leaf1_small_0.png").convert_alpha()]
        self.image = spritesheet.load_strip('leaves-rotating-88.png', 88, colorkey = None)[0]
        #print self.image

        # bough collides with ground and woger
        self.layers = LayerType.ITEMS | LayerType.PLAYER
        self.group = GroupType.BOUGH


    def get_verts(self):
        return [
            (- self.width / 2, - self.height / 2), # left top
            (+ self.width / 2, - self.height / 2), # right top
            (               0, + self.height / 2), # bottom
        ]


    def create_body(self):
        verts = self.get_verts()

        self.body = Body(self.mass, moment_for_poly(self.mass, verts))
        self.body.position = self.branch.tip()

        self.shape = Poly(self.body, verts)

        # platforms should only collide with other platforms and woger
        self.shape.layers =  self.layers
        self.shape.group = self.group
        self.shape.collision_type = CollisionType.BOUGH
        self.shape.parent = self


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)
        
        
        self.pivot = PivotJoint(self.body, self.branch.body, self.branch.tip())
        space.add(self.pivot)

    def remove_from_tree(self, space):
        space.remove(self.pivot)

    def destroy(self):
        self.status = "Collided"
        self.body.reset_forces()

      



class Woger(GameRect):

    def __init__(self, x, y, window):
        GameRect.__init__(self, x, y, 63, 74)
        #self.color = (255, 127, 0)
        self.walk_force = 0
        self.image = [image.load("data/art/left_woger_small.png").convert_alpha(), image.load("data/art/right_woger_small.png").convert_alpha()]
        self.in_air = True
        self.allowed_glide = 2
        self.allowed_jump = 1
        self.role = "Woger"
        self.status = None
        self.score = 0
        self.multiplier = 1
        # yes yes, I know! it's bad! ** He's a very naughty boy
        self.window = window

        # woger collides with ground and boughs
        self.layers = LayerType.PLAYER


        self.last_direction = 1

    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = self.layers
        self.shape.collision_type = CollisionType.PLAYER


    def _update(self):
        """not finished, please leave - Jonathan"""
        event.pump()
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.left()
        elif keys[K_RIGHT]:
            self.right()

        if keys[K_SPACE]:
            self.jump()

        if self.walk_force:
            self.do_walk()


    def update(self):
##        if self.body.position[1] >= self.window.height - 100:
##            self.body.reset_forces()
        if self.walk_force:
            self.do_walk()


    def do_walk(self, direction=None):        

        key_down = direction is not None
        if key_down:
            self.allowed_glide = max(0, self.allowed_glide-1)
        else:
            direction = copysign(1, self.walk_force)
        force = direction * self.mass

        self.body.apply_impulse((force, 0), (0, 0))
        self.walk_force += force
        if self.in_air and key_down and not self.allowed_glide:
            self.end_walk()

        self.last_direction = direction

    def end_walk(self):
        #self.body.apply_impulse((-self.walk_force*self.last_direction, 0), (0, 0))
        self.walk_force = 0


    def jump(self):
        vel_of_jump = Vec2d(0, self.mass*11)
        if self.in_air:
            Sounds.sounds.play("orange_splat")
            # half as much.
            vel_of_jump = vel_of_jump/2
        else:
            Sounds.sounds.play("jump1")

        self.body.apply_impulse(vel_of_jump, (0, 0))
        self.allowed_jump -= 1

    def dive(self):
        vel_of_dive = Vec2d(0, -self.mass*11)
        Sounds.sounds.play("dive1")
        self.body.apply_impulse(vel_of_dive, (0, 0))

class Owange(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 63, 74)
        #self.color = pygame.Color('orange')
        self.walk_force = 0
        self.image = [image.load("data/art/orange/owange.png").convert_alpha()]
        self.animation = image.load("data/art/orange/orange_splat_small.png").convert_alpha() #spritesheet.load_strip('orange_splat.png', 1362, colorkey = None)[0]
        self.in_air = True
        self.allowed_glide = 2
        self.role = "Owange"
        self.status = None
        self.deadtime = 0

        # owange collides with ground and boughs
        self.layers = LayerType.PLAYER | LayerType.ITEMS
        self.layers = 1

    def destroy(self):
        self.status = "Collided"
        self.image = [image.load("data/art/orange/orange_splat_small.png").convert_alpha()] #spritesheet.load_strip('orange_splat.png', 1362, colorkey = None)[0]
        self.body.reset_forces()

    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = self.layers
        self.shape.collision_type = CollisionType.OWANGE

class Cherry(GameRect):

    def __init__(self, x=63, y=74):
        #x = random.randint(0,550)
        #y = random.randint(0,550)
        GameRect.__init__(self, x, y, 31, 75)
        self.image = [image.load("data/art/cherry/cherry_small.png").convert_alpha()]
        #self.animation = image.load("data/art/orange/orange_splat_small.png").convert_alpha() #spritesheet.load_strip('orange_splat.png', 1362, colorkey = None)[0]
        self.in_air = True
        self.role = "Cherry"
        self.status = None
        self.deadtime = 0

        # cherry collides with ground and boughs
        self.layers = 1

    def destroy(self):
        self.status = "Collided"
        #self.image = [image.load("data/art/orange/orange_splat_small.png").convert_alpha()] #spritesheet.load_strip('orange_splat.png', 1362, colorkey = None)[0]
        self.body.reset_forces()

    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = 1
        self.shape.collision_type = CollisionType.CHERRY
