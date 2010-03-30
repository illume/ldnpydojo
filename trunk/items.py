from __future__ import division

from pymunk import Body, DampedSpring, Poly, moment_for_poly, Vec2d



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


def get_rect_verts(width, height):
    return map(Vec2d, [
        (- width / 2, - height / 2), # left top
        (- width / 2, + height / 2), # left bottom
        (+ width / 2, + height / 2), # right bottom
        (+ width / 2, - height / 2), # right top
    ])



class GameRect(object):

    def __init__(self, x, y, width, height, static=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.static = static
        verts = get_rect_verts(self.width, self.height)
        self.mass = self.width * self.height
        self.body = Body(
            self.mass, moment_for_poly(self.mass, verts))
        self.body.position = (x, y)
        self.shape = Poly(self.body, verts, (0, 0))

    @property
    def verts(self):
        return self.shape.get_points()        


class Platform(GameRect):

    def __init__(self, x, y, width=400, height=50, static=False):
        GameRect.__init__(self, x, y, width, height, static)
        self.color = (255, 255, 0)


class Woger(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 32, 32)
        self.color = (255, 127, 0)
    
