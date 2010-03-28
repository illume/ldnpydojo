
from pymunk import Space


class World(object):

    def __init__(self):
        self.items = []
        self.space = Space()

    def add(self, item):
        self.items.append(item)
        self.space.add(item.shape)
        self.space.add(item.body)

    def update(self):
        self.space.step(1)

