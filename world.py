
from pymunk import init_pymunk, Space


class World(object):

    def __init__(self):
        self.items = []
        self.springs = []
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -0.1)
        self.space.resize_static_hash()
        self.space.resize_active_hash()

    def add_item(self, item):
        self.items.append(item)
        item.create_body()
        item.add_to_space(self.space)

    def add_spring(self, spring):
        self.springs.append(spring)
        self.space.add(spring)

    def update(self):
        self.space.step(1)

