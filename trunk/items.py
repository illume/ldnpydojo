
from pymunk import Body, Poly, moment_for_poly


class Platform(object):

    def __init__(self, x, y, angle=0.0):
        self.width = 400
        self.height = 50

        verts = (
            (x - self.width / 2, y - self.height / 2),
            (x - self.width / 2, y + self.height / 2),
            (x + self.width / 2, y + self.height / 2),
            (x + self.width / 2, y - self.height / 2),
        )
        self.mass = self.width * self.height
        self.body = Body(
            self.mass, moment_for_poly(self.mass, verts))
        self.shape = Poly(self.body, verts, (0, 0))


    @property
    def x(self):
        return self.body.position.x


    @property
    def y(self):
        return self.body.position.y


    @property
    def angle(self):
        return self.body.angle


    @property
    def verts(self):
        return self.shape.get_points()



class Player(object):

    def __init__(self, x, y, angle=0.0):
        self.x = x
        self.y = y
        self.angle = angle

