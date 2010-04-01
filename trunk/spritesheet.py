"""


"""


import os
import pygame
from pygame.locals import *
import glob

import game
from cyclic_list import cyclic_list

#vec2d = tuple
import pymunk 
vec2d = pymunk.Vec2d


IMAGE_CACHE = {}

def load_image(filename, colorkey=None):
    """ colorkey - if -1, then use the top left pixel as the color.
        colorkey - if None, then use per pixel alpha images.
    """
    if filename not in IMAGE_CACHE:
        if os.path.exists(filename):
            fname = filename
        else:
            fname = os.path.join("data", "art", filename)
        img = pygame.image.load(fname)

        if colorkey is not None:
            # color key images
            if colorkey is -1:
                colorkey = img.get_at((0,0))
            img = img.convert()
            img.set_colorkey(colorkey, RLEACCEL)
        else:
            # per pixel alpha images.
            img = img.convert_alpha()

        IMAGE_CACHE[filename] = img
    return IMAGE_CACHE[filename]



def load_strip(filename, width, colorkey = None):
    imgs = []
    img = load_image(filename, colorkey)
    for x in range(img.get_width()/width):
        i = img.subsurface(pygame.Rect(x*width, 0, width, img.get_height()))
        if colorkey:
            i.set_colorkey(img.get_colorkey(), RLEACCEL)
        imgs.append(i)
    imgs.reverse()
    return imgs, img



class Strip(game.Game):


    def __init__(self,
                 filename=None,
                 width=None,
                 colorkey = None,
                 pos = None,
                 loop = -1,
                ):
        """ loop - number of times to loop.  -1 means loop forever.
        """
        game.Game.__init__(self)

        if pos is None:
            self.pos = (0,0)
            raise NotImplementedError("ok")
        else:
            self.pos = pos

        self.loop = loop
        self.filename = filename
        
        self.looped = 0
        if None not in [filename, width]:
            self.load(filename, width, colorkey)

        self.gotoBeginning()


    def load(self, filename = None, width=50, colorkey=None):

        if filename is None:return

        self.strip, self.big_image = load_strip(filename, width, colorkey)
        self.idx = 0
        self.filename = filename

        self.idx = 0
        self.image = self.strip[self.idx]

        #self.update(0)

    def gotoBeginning(self):
        self.idx = 0
        self.looped = 0

    def draw(self, screen, world = (0,0)):
        rects = game.Game.draw(self, screen)
        r = screen.blit(self.image, self.pos + world)
        return rects + [r]


    def update(self, elapsed_time):
        """ update which frame we are drawing.
        """
        game.Game.update(self, elapsed_time)

        # update which frame we are drawing.
        try:
            self.image = self.strip[self.idx]
        except IndexError:
            if self.loop == -1 or self.looped < self.loop:
                self.idx = 0
                self.image = self.strip[self.idx]
                self.looped += 1
                
            else:
                self.idx = len(self.strip)-1
                self.image = self.strip[self.idx]

        self.idx += 1
        # 
        




class Strips(game.Game):
    """multiple animation strips.




    So for a colorkey image with 100 pixel wide frames:
       somename-movement-colorkey-100.png

    For per pixel alpha transparency image with 100 pixel wide frames:
       somename-movement-100.png

    """
    def __init__(self, fnames, pos):
        game.Game.__init__(self)

        strips = cyclic_list([])
        y = 0
        for i, fname in enumerate(fnames):
            if "colorkey" in fname:
                colorkey=-1
            else:
                colorkey=None
            #pos = (50*i, y)

            # get the width out of the filename.
            parts = fname.split(".")
            try:
                width = int(parts[-2].split('-')[-1])
            except:
                width = 50
            strips.append( Strip(fname, width, colorkey, pos=pos, loop=-1) )

        self.pos = pos
        self.strips = strips
        self.strip = self.strips[0]

        self.world = vec2d(0,0)



    def set_strip(self, idx):
        pos = self.strip.pos
        self.strip = self.strips[idx]
        self.strip.pos = pos
        self.pos = pos
        self.strips.idx = idx
        print "changed to:", self.strip.filename

    def next_strip(self):
        """go to the next strip in the list.
        """
        self.strips.next()
        self.set_strip(self.strips.idx)


    def strip_name(self, name):
        """ select the first strip with the given name
        """

        ones = [(i,s) for i,s in enumerate(self.strips) if name in s.filename]
        self.set_strip( ones[0][0] )



    def draw(self, screen):
        """
        """
        
        rects = game.Game.draw(self, screen)

        # see which direction we are looking.
        #d = self.direction
        #if d.x < 0:
        #    flip_it = 1
        #else:
        #    flip_it = 0
        flip_it = 0

        # blit it according on the direction, and position in the world.
        r = screen.blit(pygame.transform.flip(self.strip.image, flip_it, 0), 
                        self.strip.pos + self.world)
        return rects + [r]
        
        
    def update(self, elapsed_time):
        game.Game.update(self, elapsed_time)
        self.strip.update(elapsed_time)
        #self.strip.pos += self.direction
        self.pos = self.strip.pos







if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((640,480))

    
    # here we just load the strip into a whole bunch of sub surfaces.
    #  sub surfaces reference the big image, but act just like normal surfaces.
    sub_surfaces = load_strip('leaf-movement-88.png', 88, colorkey = None)

    print len(sub_surfaces)
    assert(len(sub_surfaces) == 2)






    top = Strips(['leaf-movement-88.png'], (0,0))


    top.going = True
    clock = pygame.time.Clock()

    x,y = 0,0

    pygame.key.set_repeat (500, 30)
    i = 0
    while top.going:
        events = pygame.event.get()
        if [e for e in events if e.type in [QUIT, KEYDOWN]]:
            top.going = False

        top.handle_events(events)
        top.update(1./25)
        top.draw(screen)

        pygame.display.flip()
        clock.tick(25)
        #print clock.get_fps()


    

