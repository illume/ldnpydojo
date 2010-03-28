from __future__ import division

from pymunk import Body, Poly, moment_for_poly, Vec2d


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
        self.mass = self.width * self.height
        self.body = Body(
            self.mass, moment_for_poly(self.mass, verts))
        self.body.position = (x, y)
        self.shape = Poly(self.body, verts, (0, 0))


    @property
    def verts(self):
        return self.shape.get_points()

    @property
    def centre(self):
        verts = self.verts
        average = lambda ns:sum(ns)/len(ns)
        return average((verts[0].x, verts[2].x)), average((verts[0].y, verts[2].y))

    