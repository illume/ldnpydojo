
from pygame import draw, font
from items import Branch



class Camera(object):

    def __init__(self, window):
        self.window = window

    def point_to_screen(self, point):
        """ point_to_screen((x,y)) : (tx,ty) returns transformed points.
        """
        x, y = point
        w, h = self.window.width, self.window.height
        return (x+w/2, h-100-y) 

    def to_screen(self, verts):

        #return [self.point_to_screen(point) for point in verts]
        # we avoid the method calls/lookups.
        w, h = self.window.width, self.window.height
        return [(x+w/2, h-100-y) for x,y in verts]


def angle(angle):
    """ angle(angle) returns a normalised angle to 0..360
        >>> angle(361)
        1
        >>> angle(-100)
        100
    """
    return int( abs(angle) % 360 )




class Render(object):

    def __init__(self, window, world):
        self.window = window
        self.world = world
        self.camera = Camera(window)
        self.facing_right = 0
        self.font = font.SysFont(None, 48)


    def draw_world(self):
        self.window.display_surface.fill((0, 100, 255))
        # draw all branches first
        for item in self.world.items:
            if isinstance(item, Branch):
                self.draw_item(item)
        for item in self.world.items:
            if not isinstance(item, Branch):
                self.draw_item(item)
        self.draw_score()
        
    def draw_score(self):
        woger = self.world.player_character
        text = '%d' %woger.score
        self.window.display_surface.blit(
            self.font.render(text, True, (255,255,255)),
            #self.camera.point_to_screen()
            (50, 50)
            )

    def draw_item(self, item):
        if item.role == "Woger":
        #if hasattr(item, 'image'):
                #self.window.display_surface.blit(
               # item.image, self.camera.point_to_screen(item.body.position))
            if item.body.velocity[0] < -0.1:
               self.window.display_surface.blit(
               item.image[0], self.camera.point_to_screen(item.body.position))
               self.facing_right = 0
            elif item.body.velocity[0] > 0.1:
               self.window.display_surface.blit(
               item.image[1], self.camera.point_to_screen(item.body.position))
               self.facing_right = 1
            else:
               self.window.display_surface.blit(
               item.image[self.facing_right], self.camera.point_to_screen(item.body.position))
                   

        elif item.role == "Bough":
            #an_image = item.image[angle(item.body.angle)]
            #Only 16 images in there.  So we find the closest image for that angle.
            #  >>> 360 / 23
            #  15
            #  >>> 0 / 23
            #  0
            #  >>> 180 / 23
            #  7
            assert(len(item.image) == 16)
            idx_for_angle = int(angle(item.body.angle) /23)
            an_image = item.image[idx_for_angle]

##            verts = item.shape.get_points()
##            x,y = sum(v[0] for v in verts)/3, sum(v[1] for v in verts)/3
            self.window.display_surface.blit(an_image,
##                   self.camera.point_to_screen((x,y)))
                   self.camera.point_to_screen(item.body.position))

        elif item.role == "Owange":
            if item.status == "Collided":
                #print "Collided"
               self.window.display_surface.blit(
                           item.image[0], self.camera.point_to_screen(item.body.position))
            else:
                self.window.display_surface.blit(
                           item.image[0], self.camera.point_to_screen(item.body.position))
        else:
            # note: 80% of program execution time is in this clause
            # particularly retrieving the item.verts
            draw.polygon(
                self.window.display_surface,
                item.color,
                self.camera.to_screen(item.verts), 0)

