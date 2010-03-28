
from pymunk import Body, Poly, moment_for_poly, Vec2d


class Platform(object):

    def __init__(self, x, y, width=400, height=50):
        self.width = width
        self.height = height

        verts = [
            (- self.width / 2, - self.height / 2),
            (- self.width / 2, + self.height / 2),
            (+ self.width / 2, + self.height / 2),
            (+ self.width / 2, - self.height / 2),
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

