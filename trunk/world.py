
from pymunk import init_pymunk, Space


class World(object):

    def __init__(self):
        self.items = []
        init_pymunk()
        self.space = Space()
        self.space.resize_static_hash()
        self.space.resize_active_hash()


    def add(self, item):
        self.items.append(item)
        self.space.add(item.shape)
        self.space.add(item.body)

    def update(self):
        self.space.step(1.0)

