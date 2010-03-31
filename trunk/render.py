
from pygame import draw, display

from items import Branch

screen = display.set_mode()

class Camera(object):

    def __init__(self, window):
        self.window = window

    def to_screen(self, verts):
        return [(x + self.window.width / 2, self.window.height - 100 - y)
                for (x, y) in verts]



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
            print item.body.position
            screen.blit(item.Image, item.body.position)
        else:                
            draw.polygon(
                self.window.display_surface,
                item.color,
                self.camera.to_screen(item.verts), 0)

