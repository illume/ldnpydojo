
from pygame import draw, display
from pymunk import Vec2d
from items import Branch

screen = display.set_mode()

class Camera(object):

    def __init__(self, window):
        self.window = window

    def point_to_screen(self, point):
        x, y = point
        return (x + self.window.width / 2, self.window.height - 100 - y)

    def to_screen(self, verts):
        return [self.point_to_screen(point) for point in verts]

                    



class Render(object):

    def __init__(self, window, world):
        self.window = window
        self.world = world
        self.camera = Camera(window)


    def draw_world(self):
        self.window.display_surface.fill((0, 100, 255))
        for item in self.world.items:
            if isinstance(item, Branch):
                self.draw_item(item)
        for item in self.world.items:
            if not isinstance(item, Branch):
                self.draw_item(item)

    # note: 80% of gameloop execution time is in this method,
    # particularly retrieving the item.verts - Jonathan
    def draw_item(self, item):

        if item.Role == "Character":
            screen.blit(item.Image, self.camera.point_to_screen(item.body.position))
        else:                
            draw.polygon(
                self.window.display_surface,
                item.color,
                self.camera.to_screen(item.verts), 0)

