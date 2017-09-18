import logging
from enum import Enum

from numpy.core.umath import radians
from pyglet.gl import *
from pyquaternion import Quaternion

logging = logging.getLogger(__name__)


# noinspection PyArgumentList
Colors = Enum('Colors', {
    ' ': [50, 50, 50],
    'W': [255, 255, 255],
    'G': [0, 128, 0],
    'R': [255, 0, 0],
    'B': [0, 0, 255],
    'O': [255, 165, 0],
    'Y': [255, 255, 0]})

Modifiers = '\' '
Scale = 2.2


class Piece(object):
    Faces = [[2, 6, 7, 3], [0, 2, 3, 1], [0, 4, 6, 2], [4, 5, 7, 6], [5, 1, 3, 7], [0, 1, 5, 4]]
    Vertices = [-1, -1, 1,  -1, -1, -1,  -1, 1, 1,  -1, 1, -1,  1, -1, 1,  1, -1, -1,  1, 1, 1,  1, 1, -1]
    Moves = {
        'R': {'axis': 0, 'direction': -1, 'filter': (1, None, None), 'face': [3, -3, -2]},
        'L': {'axis': 0, 'direction': +1, 'filter': (-1, None, None), 'face': [1, 3, -2]},
        'U': {'axis': 1, 'direction': -1, 'filter': (None, 1, None), 'face': [0, 1, 3]},
        'D': {'axis': 1, 'direction': +1, 'filter': (None, -1, None), 'face': [5, 1, -3]},
        'F': {'axis': 2, 'direction': -1, 'filter': (None, None, 1), 'face': [2, 1, -2]},
        'B': {'axis': 2, 'direction': +1, 'filter': (None, None, -1), 'face': [4, -1, 2]},
        'X': {'axis': 0, 'direction': +1, 'filter': (None, None, None), 'face': None},
        'Y': {'axis': 1, 'direction': +1, 'filter': (None, None, None), 'face': None},
        'Z': {'axis': 2, 'direction': -1, 'filter': (None, None, None), 'face': None},
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

        self.position = (x, y, z)
        self._rotate = [0, 0, 0]
        self._animate = [0, 0, 0]
        self._scale = scale

    def __eq__(self, other):
        return self.position == other

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

        self.faces = Piece._rotate_faces(self.faces, *self._rotate)
        self.position = Piece._rotate_vertex(self.position, *self._rotate, int)
        self._rotate = [0, 0, 0]

    def draw(self):
        glPushMatrix()

        glRotatef(self._rotate[0], 1, 0, 0)
        glRotatef(self._rotate[1], 0, 1, 0)
        glRotatef(self._rotate[2], 0, 0, 1)
        glTranslatef(self.position[0] * self._scale, self.position[1] * self._scale, self.position[2] * self._scale)

        glScalef(self._scale / Scale, self._scale / Scale, self._scale / Scale)

        count = len(self._vertices) // 3
        for index, face in enumerate(Piece.Faces):
            pyglet.graphics.draw_indexed(
                count, GL_QUADS,
                face, ('v3f', self._vertices), ('c3B', self._colors[index] * count))

        glPopMatrix()

    def rotate(self, spec, speed):
        if not spec or spec[0] not in Piece.Moves:
            return False

        # only animate affected pieces
        axis_filter = Piece.Moves[spec[0]]['filter']
        for index in range(3):
            if axis_filter[index] is not None and self.position[index] != axis_filter[index]:
                return False

        axis_index = Piece.Moves[spec[0]]['axis']
        axis_angle = Piece.Moves[spec[0]]['direction'] * speed
        axis_angle = -axis_angle if len(spec) > 1 and spec[1] == '\'' else axis_angle
        self._animate[axis_index] = axis_angle
        return True

    # noinspection PyUnusedLocal
    def tick(self, *args, **kwargs):
        if not self._animate[0] and not self._animate[1] and not self._animate[2]:
            return False

        for i in range(3):
            self._rotate[i] = (self._rotate[i] + self._animate[i]) % 360
            if self._animate[i] != 0 and self._rotate[i] % 90 == 0:
                self._animate[i] = 0
                self._apply()
                return True

        return False
