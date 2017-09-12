import random
import threading
from enum import Enum
from queue import Queue

from numpy.core.umath import radians
from pyglet import clock
from pyglet.gl import *
from pyquaternion import Quaternion

# noinspection PyArgumentList
Colors = Enum('Colors', {
    ' ': [0, 0, 0],
    'W': [255, 255, 255],
    'G': [0, 128, 0],
    'R': [255, 0, 0],
    'B': [0, 0, 255],
    'O': [255, 165, 0],
    'Y': [255, 255, 0]})


class Piece(object):
    Faces = [[2, 6, 7, 3], [0, 2, 3, 1], [0, 4, 6, 2], [4, 5, 7, 6], [5, 1, 3, 7], [0, 1, 5, 4]]
    Vertices = [-1, -1, 1,  -1, -1, -1,  -1, 1, 1,  -1, 1, -1,  1, -1, 1,  1, -1, -1,  1, 1, 1,  1, 1, -1]
    Scale = 2.1
    Moves = {
        'R': {'axis': 0, 'direction': -1, 'filter': (1, None, None), 'face': [3, -3, -2]},
        'L': {'axis': 0, 'direction': +1, 'filter': (-1, None, None), 'face': [1, 3, -2]},
        'U': {'axis': 1, 'direction': -1, 'filter': (None, 1, None), 'face': [0, 1, -3]},
        'D': {'axis': 1, 'direction': +1, 'filter': (None, -1, None), 'face': [5, 1, -3]},
        'F': {'axis': 2, 'direction': -1, 'filter': (None, None, 1), 'face': [2, 1, -2]},
        'B': {'axis': 2, 'direction': +1, 'filter': (None, None, -1), 'face': [4, -1, -2]},
        'X': {'axis': 0, 'direction': +1, 'filter': (None, None, None), 'face': None},
        'Y': {'axis': 1, 'direction': +1, 'filter': (None, None, None), 'face': None},
        'Z': {'axis': 2, 'direction': +1, 'filter': (None, None, None), 'face': None},
    }

    def __init__(self, x, y, z, scale=30):
        self._vertices = Piece.Vertices[:]
        self.faces = [
            'W' if y == 1 else ' ',
            'G' if x == -1 else ' ',
            'R' if z == 1 else ' ',
            'B' if x == 1 else ' ',
            'O' if z == -1 else ' ',
            'Y' if y == -1 else ' ']
        self._colors = [Colors[c].value for c in self.faces]

        self._position = (x, y, z)
        self._rotate = [0, 0, 0]
        self._animate = [0, 0, 0]
        self._scale = scale
        self._moving = threading.Event()

    def __getitem__(self, item):
        return self.faces[item]

    @property
    def moving(self):
        return self._moving.is_set()

    @staticmethod
    def _rotate_vertex(vertex, ax, ay, az, cast=float):
        vertex = Quaternion(axis=(1, 0, 0), angle=radians(ax)).rotate(vertex)
        vertex = Quaternion(axis=(0, 1, 0), angle=radians(ay)).rotate(vertex)
        vertex = Quaternion(axis=(0, 0, 1), angle=radians(az)).rotate(vertex)
        return cast(round(vertex[0])), cast(round(vertex[1])), cast(round(vertex[2]))

    @staticmethod
    def _rotate_faces(faces, ax, ay, az):
        indexes = [0,1,2,3,4,5]
        if ax == 90: indexes = [4,1,0,3,5,2]
        elif ax == 270: indexes = [2,1,5,3,0,4]
        elif ay == 90: indexes = [0,4,1,2,3,5]
        elif ay == 270: indexes = [0,2,3,4,1,5]
        elif az == 90: indexes = [3,0,2,5,4,1]
        elif az == 270: indexes = [1,5,2,0,4,3]
        return [faces[i] for i in indexes]

    def _apply(self):
        for index in range(len(self._vertices) // 3):
            vertex = self._rotate_vertex(self._vertices[index * 3: (index + 1) * 3], *self._rotate)
            self._vertices = self._vertices[:index * 3] + list(vertex) + self._vertices[(index + 1) * 3:]
        self._position = Piece._rotate_vertex(self._position, *self._rotate, int)
        self.faces = Piece._rotate_faces(self.faces, *self._rotate)
        self._rotate = [0, 0, 0]

    def draw(self):
        glPushMatrix()

        glRotatef(self._rotate[0], 1, 0, 0)
        glRotatef(self._rotate[1], 0, 1, 0)
        glRotatef(self._rotate[2], 0, 0, 1)
        glTranslatef(self._position[0] * self._scale, self._position[1] * self._scale, self._position[2] * self._scale)

        glScalef(self._scale / Piece.Scale, self._scale / Piece.Scale, self._scale / Piece.Scale)

        count = len(self._vertices) // 3
        for index, face in enumerate(Piece.Faces):
            pyglet.graphics.draw_indexed(
                count, GL_QUADS,
                face, ('v3f', self._vertices), ('c3B', self._colors[index] * count))

        glPopMatrix()

    # noinspection PyUnusedLocal
    def tick(self, *args, **kwargs):
        for i in range(3):
            self._rotate[i] = (self._rotate[i] + self._animate[i]) % 360
            if self._animate[i] != 0 and self._rotate[i] % 90 == 0:
                self._animate[i] = 0
                self._apply()
                self._moving.clear()

    def rotate(self, spec, speed=10):
        assert 90 // speed * speed == 90, '90 must be a multiple of the speed'

        if not spec or spec[0] not in Piece.Moves:
            return

        # only animate affected pieces
        axis_filter = Piece.Moves[spec[0]]['filter']
        for index in range(3):
            if axis_filter[index] is not None and self._position[index] != axis_filter[index]:
                return

        # animate
        self._moving.set()
        axis_index = Piece.Moves[spec[0]]['axis']
        axis_angle = Piece.Moves[spec[0]]['direction'] * speed
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
        return list(Piece.Moves.keys())

    def draw(self):
        for piece in self.pieces:
            piece.draw()

    def shuffle(self, count=10, speed=15):
        command = ''
        for _ in range(count):
            move = random.choice([m for m in self.moves if m not in 'XYZ'])
            modifier = random.choice(RubiksCube.Modifiers)
            command += '{}{} '.format(move, modifier.strip())
        self.do(command, speed=speed)

    def do(self, commands, speed=5):
        for command in commands.split(' '):
            self._commands.put((command, speed))

    def tick(self, ts, *args, **kwargs):
        if not self._commands.empty() and all(not piece.moving for piece in self.pieces):
            command, speed = self._commands.get()
            for cube in self.pieces:
                cube.rotate(command, speed)

        for cube in self.pieces:
            cube.tick(*args, **kwargs)

    def __getitem__(self, item):
        return [p for p in self.pieces if p._position == item][0]

    def face(self, face):
        axis = Piece.Moves[face]['axis']
        expected = Piece.Moves[face]['filter'][axis]
        face_info = Piece.Moves[face]['face']

        pieces = []
        coord = [expected, expected, expected]
        for j in range(-1,2):
            for i in range(-1,2):
                coord[abs(face_info[1]) - 1] = i if face_info[1] > 0 else 0 - i
                coord[abs(face_info[2]) - 1] = j if face_info[2] > 0 else 0 - j
                pieces.append(self[tuple(coord)])

        return ''.join(p.faces[face_info[0]] for p in pieces)

    def __str__(self):
        return ', '.join(self.face(f) for f in 'ULFRBD')
