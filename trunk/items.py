from __future__ import division

from pymunk import (
    Body, DampedRotarySpring, DampedSpring, PivotJoint, Poly, moment_for_poly,
    Vec2d,
)


class Spring(DampedSpring):

    def __init__(self,
        p1, p2,
        verts_to_anchor1, verts_to_anchor2,
        rest_length, stiffness, damping
    ):
        self.p1 = p1
        self.p2 = p2
        
        self.verts_to_anchor1 = verts_to_anchor1
        self.verts_to_anchor2 = verts_to_anchor2
        
        offset1 = verts_to_anchor1(p1.verts) - (p1.x, p1.y)
        offset2 = verts_to_anchor2(p2.verts) - (p2.x, p2.y)

        super(Spring, self).__init__(
            p1.body, p2.body,
            offset1, offset2,
            rest_length, stiffness, damping)



class GameRect(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = self.width * self.height


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


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)


    @property
    def verts(self):
        return self.shape.get_points()        



class Ground(GameRect):

    def __init__(self):
        GameRect.__init__(self, 0, -1000, 2000, 2000)
        self.mass = 1e100
        self.color = (0, 255, 0)


    def add_to_space(self, space):
        # give ground a group, so it will not collide with trunk, which will
        # overlap it slightly at the base
        self.shape.group = 1
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

        # branch should not collide with its parent, with which it will
        # overlap slightly at the joint
        self.shape.group = self.parent.shape.group


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)
        trunkPivot = PivotJoint(self.body, self.parent.body, self.tail())
        space.add(trunkPivot)
        trunkSpring = DampedRotarySpring(
            self.body, self.parent.body, 0.0, self.mass * 5000, self.mass)
        space.add(trunkSpring)



class Woger(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 32, 32)
        self.color = (255, 127, 0)
    
