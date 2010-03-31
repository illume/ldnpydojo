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
        self.mass = self.width * self.height / 10
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

        # ground should collide with everything (layers 1 & 2)
        self.layers = 3

    def add_to_space(self, space):
        # give ground a group, so it will not collide with trunk, which will
        # overlap it slightly at the base
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


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)
        pivot = PivotJoint(self.body, self.parent.body, self.tail())
        space.add(pivot)
        spring = DampedRotarySpring(
            self.body, self.parent.body, 0.0, self.mass * 1000, self.mass)
        space.add(spring)


class Bough(GameRect):

    def __init__(self, branch):
        self.branch = branch
        x, y = branch.tip()
        GameRect.__init__(self, x, y, 100, 25)
        self.color = (0, 255, 0)

        # bough collides with ground and woger
        self.layers = 1

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


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)
        
        pivot = PivotJoint(self.body, self.branch.body, self.branch.tip())
        space.add(pivot)


class Woger(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 32, 32)
        self.color = (255, 127, 0)

        # woger collides with ground and boughs
        self.layers = 1

    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = 1

