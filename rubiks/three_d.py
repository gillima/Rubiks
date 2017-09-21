import threading

from pyglet import clock
from pyglet.gl import *

from .config import *
from .text import Cube as TextCube


class Piece(object):
    def __init__(self, x, y, z, cube):
        self._position = (x, y, z)
        self._colors = []
        self._position_scale = CubeSize / 3
        self._piece_size = (CubeSize / 6) * PieceScale
        self.apply_colors(cube)

    @property
    def position(self):
        return self._position

    def apply_colors(self, cube):
        self._colors = [Colors[c] for c in cube.get_colors(*self._position)]

    def draw(self):
        glPushMatrix()
        glTranslatef(
            self._position[0] * self._position_scale,
            self._position[1] * self._position_scale,
            self._position[2] * self._position_scale)
        glScalef(
            self._piece_size,
            self._piece_size,
            self._piece_size)
        for index, face in enumerate(Faces):
            pyglet.graphics.draw_indexed(
                8, GL_QUADS, face,
                ('v3f', Vertices),
                ('c3B', self._colors[index] * 8))
        glPopMatrix()


class Cube(TextCube):
    """
    OpenGL version to draw a 3D Rubik's Cube.
    """
    def __init__(self):
        super().__init__()
        self._pieces = [Piece(x, y, z, self)
                        for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)
                        if x or y or z]
        self._rotate = [0, 0, 0]
        self._animated = []
        self._speed = None
        self._stable = self._pieces[:]
        self._idle = threading.Semaphore()

    def draw(self):
        glPushMatrix()

        for piece in self._stable:
            piece.draw()

        glRotatef(self._rotate[0], 1, 0, 0)
        glRotatef(self._rotate[1], 0, 1, 0)
        glRotatef(self._rotate[2], 0, 0, 1)

        for piece in self._animated:
            piece.draw()

        glPopMatrix()

    def update(self, command, front, inverse, speed):
        self._idle.acquire()
        if speed == Speed.Immediate:
            self._finish_update()
            return

        axis = Animation[command]['axis']
        direction = speed.value * Animation[command]['dir']
        if not inverse:
            direction = -direction
        self._speed = [0, 0, 0]
        self._speed[axis] = direction

        face = Animation[command]['face']
        for piece in self._pieces:
            if face is None or piece.position[axis] == face:
                self._stable.remove(piece)
                self._animated.append(piece)

        clock.schedule_interval(self._tick, interval=0.01)

    def _finish_update(self):
        self._rotate = [0, 0, 0]
        self._speed = None

        for piece in self._pieces:
            piece.apply_colors(self)

        self._idle.release()

    def _tick(self, ts, *args, **kwargs):
        if self._speed:
            self._rotate[0] = self._rotate[0] + self._speed[0]
            self._rotate[1] = self._rotate[1] + self._speed[1]
            self._rotate[2] = self._rotate[2] + self._speed[2]

        if all(r % 90 == 0 for r in self._rotate):
            self._animated = []
            self._stable = list(self._pieces)
            clock.unschedule(self._tick)
            self._finish_update()
