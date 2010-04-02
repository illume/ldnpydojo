
from __future__ import division

from math import copysign

import pygame

from pygame import event, image, key
from pymunk import (
    Body, DampedRotarySpring, PivotJoint, Poly, moment_for_poly, Vec2d,
)

from sounds import Sounds
import spritesheet



class GameRect(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = self.width * self.height / 10000
        self.layers = -1 # collide with everything


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



class CollisionType:
    GROUND, BOUGH, PLAYER, BRANCH, OWANGE = range(5)



class Ground(GameRect):

    def __init__(self):
        GameRect.__init__(self, 0, -1000, 2000, 2000)
        self.mass = 1e100
        self.color = (0, 255, 0)
        # ground should collide with everything (3 = 1 || 2)
        self.layers = 3
        self.role = "Ground"

    def add_to_space(self, space):
        self.shape.collision_type = CollisionType.GROUND
        space.add_static(self.shape)


class BoundingTrunk(GameRect):

    def __init__(self, x):
        GameRect.__init__(self, x, 1000, 50, 2000)
        self.mass = 1e100
        self.color = (128, 64, 0)
        self.layers = 3  # collide with everything
        self.role = "BoundingTrunk"

    def add_to_space(self, space):
        # TODO: more interesting collision to allow ninja double jumps
        self.shape.collision_type = CollisionType.GROUND
        space.add_static(self.shape)


class Branch(GameRect):
    
    def __init__(self, parent, angle, width=None, height=None):
        self.parent = parent
        self.angle = angle
        if width == None:
            width = parent.width / 2
        if height == None:
            height = parent.height / 2
        GameRect.__init__(self, 0, height / 2, width, height)
        self.color = (128, 64, 0)
        self.role = "Branch"

        # branches should only collide with ground
        self.layers = 2


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
        self.shape.group = 1

        # branches should collide only with ground
        self.shape.layers = 2
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
        #self.image = [image.load("data/art/leaves/leaf1_small_0.png").convert_alpha()]
        self.image = spritesheet.load_strip('leaves-rotating-88.png', 88, colorkey = None)[0]
        #print self.image
        #raise 'asdf'

        # bough collides with ground and woger
        self.layers = 1
        self.group = 2


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


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)
        
        pivot = PivotJoint(self.body, self.branch.body, self.branch.tip())
        space.add(pivot)



class Woger(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 63, 74)
        self.color = (255, 127, 0)
        self.walk_force = 0
        self.image = [image.load("data/art/left_woger_small.png").convert_alpha(), image.load("data/art/right_woger_small.png").convert_alpha()]
        self.in_air = True
        self.allowed_glide = 2
        self.allowed_jump = 1
        self.role = "Woger"

        # woger collides with ground and boughs
        self.layers = 1


    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = 1
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


    def _left(self):
        """not finished, please leave - Jonathan"""
        if self.allowed_glide or not self.in_air:
            self.do_walk(-1)


    def _right(self):
        """not finished, please leave - Jonathan"""
        if self.allowed_glide or not self.in_air:
            self.do_walk(+1)


    def _jump(self):
        """not finished, please leave - Jonathan"""
        if not self.in_air:
            self.body.apply_impulse((0, self.mass*11), (0, 0))
            Sounds.sounds.play("jump1")


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


    def end_walk(self):
        self.body.apply_impulse((-self.walk_force, 0), (0, 0))
        self.walk_force = 0


    def jump(self):
        vel_of_jump = (0, self.mass*11)

        if self.in_air:
            Sounds.sounds.play("orange_splat")
            # half as much.
            vel_of_jump = (vel_of_jump[0]/2, vel_of_jump[1]/2)
        else:
            Sounds.sounds.play("jump1")

        self.body.apply_impulse(vel_of_jump, (0, 0))
        self.allowed_jump -= 1






class Owange(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 63, 74)
        #self.color = pygame.Color('orange')
        self.walk_force = 0
        self.image = [image.load("data/art/orange/owange.png").convert_alpha()]
        self.in_air = True
        self.allowed_glide = 2
        self.role = "Owange"

        # woger collides with ground and boughs
        self.layers = 1


    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = 1
        self.shape.collision_type = CollisionType.OWANGE


