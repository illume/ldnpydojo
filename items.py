
from __future__ import division

from math import copysign

import pygame

from pygame import event, image, key
from pymunk import (
    Body, DampedRotarySpring, PivotJoint, Poly, moment_for_poly, Vec2d,
)

from sounds import Sounds
import spritesheet



class GameRect(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = self.width * self.height / 10000
        self.layers = -1 # collide with everything


    def get_verts(self):
        return [
            (+ self.width / 2, - self.height / 2), # right bottom
            (- self.width / 2, - self.height / 2), # left bottom
            (- self.width / 2, + self.height / 2), # left top
            (+ self.width / 2, + self.height / 2), # right top
        ]


    def create_body(self):
        verts = map(Vec2d, self.get_verts())
        self.body = Body(self.mass, moment_for_poly(self.mass, verts))
        self.body.position = (self.x, self.y)
        self.shape = Poly(self.body, verts, (0, 0))
        self.shape.layers = self.layers


    def update(self):
        pass


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)


    @property
    def verts(self):
        "This is the position of the item's verts as calculated by pymunk"
        return self.shape.get_points()        



class CollisionType:
    GROUND, BOUGH, PLAYER, BRANCH, ORANGE = range(5)



class Ground(GameRect):

    def __init__(self):
        GameRect.__init__(self, 0, -1000, 2000, 2000)
        self.mass = 1e100
        self.color = (0, 255, 0)
        # ground should collide with everything (3 = 1 || 2)
        self.layers = 3
        self.role = "Ground"

    def add_to_space(self, space):
        self.shape.collision_type = CollisionType.GROUND
        space.add_static(self.shape)



class Branch(GameRect):
    
    def __init__(self, parent, angle, width=None, height=None):
        self.parent = parent
        self.angle = angle
        if width == None:
            width = parent.width / 2
        if height == None:
            height = parent.height / 2
        GameRect.__init__(self, 0, height / 2, width, height)
        self.color = (128, 64, 0)
        self.role = "Branch"

        # branches should only collide with ground
        self.layers = 2


    def rotate_verts_about(self, verts, angle, pivot):
        return [
            (vert + pivot).rotated(angle) - pivot
            for vert in verts
        ]

    def get_verts(self):
        verts = GameRect.get_verts(self)
        tail = self.tail(verts)
        return self.rotate_verts_about(verts, self.angle, tail)

    def tip(self):
        return self.midpoint(2, 3)

    def tail(self, verts=None):
        return self.midpoint(0, 1, verts)

    def midpoint(self, v1, v2, verts=None):
        if verts is None:
            verts = self.verts
        return ( Vec2d(verts[v1]) + Vec2d(verts[v2]) ) / 2


    def create_body(self):
        verts = self.get_verts()

        self.body = Body(self.mass, moment_for_poly(self.mass, verts))
        root = Vec2d(0, 0)
        if isinstance(self.parent, Branch):
            root = self.parent.tip()
        self.body.position = root - self.tail(verts)

        self.shape = Poly(self.body, verts)

        # branch should not collide with other branches, which will
        # overlap slightly at the joints
        self.shape.group = 1

        # branches should collide only with ground
        self.shape.layers = 2
        self.collision_type = CollisionType.BRANCH


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)

        pivot = PivotJoint(self.body, self.parent.body, self.tail())
        space.add(pivot)

        spring = DampedRotarySpring(
            self.body, self.parent.body, 0.0, self.mass * 10000, self.mass/10)
        space.add(spring)



class Bough(GameRect):

    def __init__(self, branch):
        self.branch = branch
        x, y = branch.tip()
        width = branch.height
        height = width / 4
        GameRect.__init__(self, x, y, width, height)
        self.color = (0, 255, 0)
        self.role = "Bough"
        #self.image = [image.load("data/art/leaves/leaf1_small_0.png").convert_alpha()]
        self.image = spritesheet.load_strip('leaves-rotating-88.png', 88, colorkey = None)[0]
        #print self.image
        #raise 'asdf'

        """image.load("data/art/leaves/leaf1_small_1.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_2.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_3.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_4.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_5.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_6.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_7.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_8.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_9.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_10.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_11.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_12.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_13.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_14.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_15.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_16.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_17.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_18.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_19.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_20.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_21.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_22.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_23.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_24.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_25.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_26.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_27.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_28.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_29.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_30.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_31.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_32.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_33.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_34.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_35.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_36.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_37.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_38.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_39.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_40.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_41.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_42.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_43.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_44.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_45.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_46.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_47.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_48.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_49.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_50.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_51.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_52.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_53.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_54.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_55.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_56.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_57.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_58.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_59.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_60.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_61.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_62.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_63.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_64.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_65.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_66.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_67.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_68.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_69.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_70.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_71.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_72.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_73.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_74.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_75.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_76.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_77.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_78.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_79.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_80.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_81.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_82.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_83.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_84.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_85.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_86.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_87.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_88.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_89.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_90.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_91.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_92.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_93.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_94.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_95.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_96.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_97.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_98.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_99.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_100.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_101.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_102.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_103.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_104.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_105.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_106.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_107.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_108.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_109.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_110.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_111.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_112.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_113.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_114.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_115.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_116.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_117.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_118.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_119.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_120.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_121.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_122.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_123.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_124.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_125.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_126.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_127.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_128.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_129.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_130.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_131.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_132.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_133.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_134.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_135.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_136.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_137.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_138.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_139.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_140.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_141.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_142.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_143.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_144.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_145.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_146.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_147.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_148.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_149.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_150.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_151.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_152.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_153.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_154.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_155.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_156.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_157.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_158.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_159.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_160.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_161.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_162.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_163.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_164.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_165.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_166.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_167.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_168.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_169.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_170.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_171.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_172.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_173.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_174.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_175.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_176.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_177.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_178.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_179.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_180.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_181.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_182.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_183.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_184.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_185.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_186.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_187.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_188.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_189.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_190.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_191.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_192.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_193.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_194.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_195.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_196.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_197.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_198.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_199.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_200.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_201.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_202.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_203.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_204.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_205.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_206.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_207.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_208.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_209.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_210.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_211.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_212.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_213.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_214.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_215.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_216.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_217.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_218.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_219.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_220.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_221.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_222.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_223.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_224.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_225.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_226.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_227.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_228.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_229.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_230.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_231.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_232.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_233.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_234.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_235.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_236.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_237.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_238.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_239.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_240.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_241.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_242.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_243.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_244.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_245.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_246.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_247.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_248.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_249.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_250.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_251.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_252.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_253.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_254.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_255.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_256.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_257.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_258.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_259.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_260.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_261.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_262.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_263.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_264.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_265.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_266.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_267.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_268.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_269.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_270.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_271.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_272.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_273.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_274.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_275.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_276.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_277.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_278.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_279.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_280.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_281.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_282.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_283.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_284.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_285.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_286.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_287.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_288.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_289.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_290.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_291.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_292.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_293.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_294.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_295.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_296.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_297.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_298.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_299.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_300.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_301.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_302.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_303.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_304.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_305.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_306.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_307.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_308.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_309.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_310.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_311.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_312.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_313.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_314.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_315.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_316.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_317.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_318.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_319.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_320.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_321.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_322.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_323.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_324.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_325.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_326.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_327.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_328.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_329.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_330.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_331.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_332.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_333.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_334.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_335.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_336.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_337.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_338.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_339.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_340.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_341.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_342.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_343.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_344.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_345.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_346.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_347.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_348.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_349.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_350.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_351.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_352.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_353.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_354.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_355.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_356.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_357.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_358.png").convert_alpha(),
image.load("data/art/leaves/leaf1_small_359.png").convert_alpha(),]
"""

        # bough collides with ground and woger
        self.layers = 1
        self.group = 2


    def get_verts(self):
        return [
            (- self.width / 2, - self.height / 2), # left top
            (+ self.width / 2, - self.height / 2), # right top
            (               0, + self.height / 2), # bottom
        ]


    def create_body(self):
        verts = self.get_verts()

        self.body = Body(self.mass, moment_for_poly(self.mass, verts))
        self.body.position = self.branch.tip()

        self.shape = Poly(self.body, verts)

        # platforms should only collide with other platforms and woger
        self.shape.layers =  self.layers
        self.shape.group = self.group
        self.shape.collision_type = CollisionType.BOUGH


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)
        
        pivot = PivotJoint(self.body, self.branch.body, self.branch.tip())
        space.add(pivot)



class Woger(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 63, 74)
        self.color = (255, 127, 0)
        self.walk_force = 0
        self.image = [image.load("data/art/right_woger_small.png").convert_alpha(), image.load("data/art/left_woger_small.png").convert_alpha()]
        self.in_air = True
        self.allowed_glide = 2
        self.role = "Woger"

        # woger collides with ground and boughs
        self.layers = 1


    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = 1
        self.shape.collision_type = CollisionType.PLAYER


    def _update(self):
        """not finished, please leave - Jonathan"""
        event.pump()
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.left()
        elif keys[K_RIGHT]:
            self.right()

        if keys[K_SPACE]:
            self.jump()

        if self.walk_force:
            self.do_walk()


    def _left(self):
        """not finished, please leave - Jonathan"""
        if self.allowed_glide or not self.in_air:
            self.do_walk(-1)


    def _right(self):
        """not finished, please leave - Jonathan"""
        if self.allowed_glide or not self.in_air:
            self.do_walk(+1)


    def _jump(self):
        """not finished, please leave - Jonathan"""
        if not self.in_air:
            self.body.apply_impulse((0, self.mass*11), (0, 0))
            Sounds.sounds.play("jump1")


    def do_walk(self, direction=None):
        key_down = direction is not None
        if key_down:
            self.allowed_glide = max(0, self.allowed_glide-1)
        else:
            direction = copysign(1, self.walk_force)
        force = direction * self.mass
        self.body.apply_impulse((force, 0), (0, 0))
        self.walk_force += force
        if self.in_air and key_down and not self.allowed_glide:
            self.end_walk()


    def end_walk(self):
        self.body.apply_impulse((-self.walk_force, 0), (0, 0))
        self.walk_force = 0


    def jump(self):
        self.body.apply_impulse((0, self.mass*11), (0, 0))
        Sounds.sounds.play("jump1")






#TODO: I don't really know how to add orange... but here is a start.
class Owange(GameRect):

    def __init__(self, x, y):
        GameRect.__init__(self, x, y, 63, 74)
        self.color = pygame.Color('orange')
        self.walk_force = 0
        self.image = [image.load("data/art/right_woger_small.png").convert_alpha(), image.load("data/art/left_woger_small.png").convert_alpha()]
        self.in_air = True
        self.allowed_glide = 2
        self.role = "Woger"

        # woger collides with ground and boughs
        self.layers = 1


    def create_body(self):
        GameRect.create_body(self)
        self.shape.layer = 1
        self.shape.collision_type = CollisionType.ORANGE


