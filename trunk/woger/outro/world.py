
from pymunk import init_pymunk, Space


class World(object):

    def __init__(self):
        self.items = []
        self.words = []
        self.springs = []
        init_pymunk()
        self.space = Space()
        self.space.resize_static_hash()
        self.space.resize_active_hash()

    def add_item(self, item):
##        self.items.append(item)
        self.space.add(item.shape)
        self.space.add(item.body)

    def add_spring(self, spring):
        self.springs.append(spring)
        self.space.add(spring)


    def add_word(self, word):
        self.words.append(word)

    def update(self):
        self.space.step(1.0)

