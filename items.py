from __future__ import division

from pymunk import Body, DampedSpring, Poly, moment_for_poly, Vec2d



class Spring(DampedSpring):

    def __init__(self, p1, p2, offset1, offset2, verts_to_anchor1, verts_to_anchor2, rest_length, stiffness, damping):    
        self.p1 = p1
        self.p2 = p2
        self.verts_to_anchor1 = verts_to_anchor1
        self.verts_to_anchor2 = verts_to_anchor2
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
        return self.mid_point(verts[0], verts[2])

    
    @staticmethod
    def point_offset_to_abs(vec, centre):
        return vec[0]+centre[0], vec[1]+centre[1]
    @staticmethod
    def verts_offset_to_abs(verts, centre):
        return [self.point_offset_to_abs(vec, self.centre) for vec in verts]


    @staticmethod
    def point_abs_to_offset(point, centre):
        return point[0]-centre[0], point[1]-centre[1]
    @staticmethod
    def verts_abs_to_offset(points, centre):
        return [self.point_abs_to_offset(point, self.centre) for point in points]    



    @staticmethod
    def mid_point(vec1, vec2):
        average = lambda ns:sum(ns)/len(ns)
        return average((vec1.x, vec2.x)), average((vec1.y, vec2.y))

        
    @property
    def abs_mid_left_end(self):
        verts = self.verts
        return self.mid_point(verts[0], verts[1])
    
    @property
    def abs_mid_right_end(self):
        verts = self.verts
        return self.mid_point(verts[2], verts[3])


    @property
    def offset_mid_left_end(self):
        return self.point_abs_to_offset(self.abs_mid_left_end, self.centre)
    
    @property
    def offset_mid_right_end(self):
        return self.point_abs_to_offset(self.abs_mid_right_end, self.centre)
        