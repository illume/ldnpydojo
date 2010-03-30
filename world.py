
from pymunk import init_pymunk, Space


class World(object):

    def __init__(self):
        self.items = []
        self.springs = []
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, 0.1)
        self.space.resize_static_hash()
        self.space.resize_active_hash()

    def add_item(self, item):
        self.items.append(item)
        if item.static:
            self.space.add_static(item.shape)
        else:
            self.space.add(item.body)
            self.space.add(item.shape)

    def add_spring(self, spring):
        self.springs.append(spring)
        self.space.add(spring)

    def update(self):
        self.space.step(1.0)

