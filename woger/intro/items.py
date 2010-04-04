from __future__ import division

from pymunk import Body, DampedSpring, Poly, moment_for_poly, Vec2d
from pygame.locals import *
from pygame import image

class Spring(DampedSpring):

    def __init__(self, p1, p2,
                 verts_to_anchor1, verts_to_anchor2,
                 rest_length, stiffness, damping):    
        self.p1 = p1
        self.p2 = p2
        
        self.verts_to_anchor1 = verts_to_anchor1
        self.verts_to_anchor2 = verts_to_anchor2
        
        offset1 = verts_to_anchor1(p1.verts) - p1.centre
        offset2 = verts_to_anchor2(p2.verts) - p2.centre

        super(Spring, self).__init__(p1.body, p2.body, offset1, offset2, rest_length, stiffness, damping)


class Platform(object):

    def __init__(self, x, y, width=400, height=50):
        self.width = width
        self.height = height

        verts = [
            (- self.width / 2, - self.height / 2),# left top
            (- self.width / 2, + self.height / 2),# left bottom
            (+ self.width / 2, + self.height / 2),# right bottom
            (+ self.width / 2, - self.height / 2),# right top
        ]
        verts = map(Vec2d, verts)
        self.mass = self.width * self.height * 1
        self.body = Body(
            self.mass, moment_for_poly(self.mass, verts))
        self.body.position = (x, y)
        self.start_pos = Vec2d(x, y)
        self.shape = Poly(self.body, verts, (0, 0))


    @property
    def verts(self):
        return self.shape.get_points()        

    @property
    def centre(self):
        verts = self.verts
        return (verts[0] + verts[2]) / 2

class Word(object):

    def __init__(self, platform, surface, start_pos):
        self.platform = platform
        self.image = surface
        self.offset = platform.start_pos - Vec2d(start_pos)

    