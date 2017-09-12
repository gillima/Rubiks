import random
import threading
from queue import Queue

from numpy.core.umath import radians
from pyglet import clock
from pyglet.gl import *
from pyquaternion import Quaternion


class Piece(object):
    Faces = [[2, 6, 7, 3], [0, 2, 3, 1], [0, 4, 6, 2], [4, 5, 7, 6], [5, 1, 3, 7], [0, 1, 5, 4]]
    Colors = [[255, 255, 255], [0, 128, 0], [255, 0, 0], [0, 0, 255], [255, 128, 0], [255, 255, 0]]
    AxisSpec = {
        'R': {'axis': 0, 'direction': -1, 'filter': (1, None, None)},
        'L': {'axis': 0, 'direction': +1, 'filter': (-1, None, None)},
        'U': {'axis': 1, 'direction': -1, 'filter': (None, 1, None)},
        'D': {'axis': 1, 'direction': +1, 'filter': (None, -1, None)},
        'F': {'axis': 2, 'direction': -1, 'filter': (None, None, 1)},
        'B': {'axis': 2, 'direction': +1, 'filter': (None, None, -1)},
        'X': {'axis': 0, 'direction': +1, 'filter': (None, None, None)},
        'Y': {'axis': 1, 'direction': +1, 'filter': (None, None, None)},
        'Z': {'axis': 2, 'direction': +1, 'filter': (None, None, None)},
    }

    def __init__(self, x, y, z, scale=30):
        self._vertices = [-1, -1, 1,  -1, -1, -1,  -1, 1, 1,  -1, 1, -1,  1, -1, 1,  1, -1, -1,  1, 1, 1,  1, 1, -1]
        self._position = [x, y, z]
        self._rotate = [0, 0, 0]
        self._animate = [0, 0, 0]
        self._scale = scale
        self._moving = threading.Event()

    @property
    def moving(self):
        return self._moving.is_set()

    @staticmethod
    def _rotate_vertex(vertex, ax, ay, az):
        vertex = Quaternion(axis=(1, 0, 0), angle=radians(ax)).rotate(vertex)
        vertex = Quaternion(axis=(0, 1, 0), angle=radians(ay)).rotate(vertex)
        vertex = Quaternion(axis=(0, 0, 1), angle=radians(az)).rotate(vertex)
        return round(vertex[0]), round(vertex[1]), round(vertex[2])

    def _apply_current(self):
        for index in range(len(self._vertices) // 3):
            vertex = self._rotate_vertex(self._vertices[index * 3: (index + 1) * 3], *self._rotate)
            self._vertices = self._vertices[:index * 3] + list(vertex) + self._vertices[(index + 1) * 3:]
        self._position = self._rotate_vertex(self._position, *self._rotate)
        self._rotate = [0, 0, 0]

    def draw(self):
        glPushMatrix()

        glRotatef(self._rotate[0], 1, 0, 0)
        glRotatef(self._rotate[1], 0, 1, 0)
        glRotatef(self._rotate[2], 0, 0, 1)
        glTranslatef(self._position[0] * self._scale, self._position[1] * self._scale, self._position[2] * self._scale)

        glScalef(self._scale / 2.05, self._scale / 2.05, self._scale / 2.05)

        count = len(self._vertices) // 3
        for index, face in enumerate(Piece.Faces):
            pyglet.graphics.draw_indexed(
                count, GL_QUADS,
                face, ('v3f', self._vertices), ('c3B', Piece.Colors[index] * count))

        glPopMatrix()

    # noinspection PyUnusedLocal
    def tick(self, *args, **kwargs):
        for i in range(3):
            self._rotate[i] = (self._rotate[i] + self._animate[i]) % 360
            if self._animate[i] != 0 and self._rotate[i] % 90 == 0:
                self._animate[i] = 0
                self._apply_current()
                self._moving.clear()

    def rotate(self, spec, speed=10):
        assert 90 // speed * speed == 90, '90 must be a multiple of the speed'

        if not spec or spec[0] not in Piece.AxisSpec:
            return

        # only animate affected pieces
        axis_filter = Piece.AxisSpec[spec[0]]['filter']
        for index in range(3):
            if axis_filter[index] is not None and self._position[index] != axis_filter[index]:
                return

        # animate
        self._moving.set()
        axis_index = Piece.AxisSpec[spec[0]]['axis']
        axis_angle = Piece.AxisSpec[spec[0]]['direction'] * speed
        axis_angle = -axis_angle if len(spec) > 1 and spec[1] == '\'' else axis_angle
        self._animate[axis_index] = axis_angle


class RubiksCube(object):
    Modifiers = '\' '

    def __init__(self):
        self.pieces = list(Piece(x - 1, y - 1, z - 1)
                           for x in range(3) for y in range(3) for z in range(3)
                           if x != 1 or y != 1 or z != 1)
        self._commands = Queue()
        clock.schedule_interval(self.tick, interval=0.01)

    @property
    def moves(self):
        return list(Piece.AxisSpec.keys())

    def draw(self):
        for piece in self.pieces:
            piece.draw()

    def shuffle(self, count=10, speed=30):
        command = ''
        for _ in range(count):
            move = random.choice([m for m in self.moves if m not in 'XYZ'])
            modifier = random.choice(RubiksCube.Modifiers)
            command += '{}{} '.format(move, modifier.strip())
        self.do(command, speed=speed)

    def do(self, commands, speed=10):
        for command in commands.split(' '):
            self._commands.put((command, speed))

    def tick(self, ts, *args, **kwargs):
        if not self._commands.empty() and all(not piece.moving for piece in self.pieces):
            command, speed = self._commands.get()
            for cube in self.pieces:
                cube.rotate(command, speed)

        for cube in self.pieces:
            cube.tick(*args, **kwargs)

