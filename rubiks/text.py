import random

from .command import Command
from .config import *


class Cube(object):
    """
    Text representation of a Rubik's Cube. The faces of the cubes are represented by a list of lists
    where each piece face is represented by a number from 1..6. The number represents the color of the pieces face.
    The order of the faces is U, L, F, R, B, D and the order of the pieces is from top left to bottom right.
    """
    def __init__(self):
        """Initializes a new instance of the :class:Cube: class. """
        self._faces = [[1] * 9, [2] * 9, [3] * 9, [4] * 9, [5] * 9, [6] * 9]
        # self._faces = [[1] * 9 + [2] * 9 + [3] * 9 + [4] * 9 + [5] * 9 + [6] * 9]

    def __str__(self):
        """Gets the text representation of all cube faces.
        >>> cube = Cube()
        >>> print(cube)
        111111111, 222222222, 333333333, 444444444, 555555555, 666666666
        """
        return ', '.join([''.join(str(c) for c in face) for face in self._faces])

    def create_commands(self, commands):
        for command in commands.split(' '):
            yield Command(self, command)

    def do(self, commands, **kwargs):
        for command in self.create_commands(commands):
            command(**kwargs)

    def get_colors(self, x, y, z):
        x1 = x + 1
        y1 = y + 1
        z1 = z + 1
        return [
            self._faces[0][x1 + z1 * 3] if y == +1 else 0,
            self._faces[1][z1 + (2 - y1) * 3] if x == -1 else 0,
            self._faces[2][x1 + (2 - y1) * 3] if z == +1 else 0,
            self._faces[3][(2 - z1) + (2 - y1) * 3] if x == +1 else 0,
            self._faces[4][x1 + (2 - y1) * 3] if z == -1 else 0,
            self._faces[5][x1 + (2 - z1) * 3] if y == -1 else 0]

    def print(self):
        for row in range(3):
            print('       {}'.format(' '.join(str(i) for i in self._faces[0][row * 3:row * 3 + 3])))
        for row in range(3):
            print('{}  {}  {}  {}'.format(
                ' '.join(str(i) for i in self._faces[1][row * 3:row * 3 + 3]),
                ' '.join(str(i) for i in self._faces[2][row * 3:row * 3 + 3]),
                ' '.join(str(i) for i in self._faces[3][row * 3:row * 3 + 3]),
                ' '.join(str(i) for i in self._faces[4][row * 3:row * 3 + 3][::-1])))
        for row in range(3):
            print('       {}'.format(' '.join(str(i) for i in self._faces[5][row * 3:row * 3 + 3])))

    def shuffle(self, count=10, speed=Speed.Fast):
        commands = ' '.join('{}{}'.format(
            random.choice('ULFRBDMES'),
            'i' if random.randrange(5) == 0 else '') for _ in range(count))

        for command in self.create_commands(commands.strip()):
            command(speed=speed)

    def update(self, command, front, inverse, speed):
        pass
