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
        """ Initializes a new instance of the :class:`Cube` class. """
        self._faces = [1] * 9 + [2] * 9 + [3] * 9 + [4] * 9 + [5] * 9 + [6] * 9

    def __str__(self):
        """ Gets the text representation of all cube faces. """
        return ', '.join([''.join(str(c) for c in self._faces[face * 6:face * 6 + 9]) for face in range(6)])

    def create_commands(self, commands):
        """ Create :class:Command: instances for all given cube notation commands """
        for command in commands.strip().split(' '):
            yield Command(self, command)

    def get_colors(self, x, y, z):
        """ Get the face colors for the piece at the given position. """
        x1 = x + 1
        y1 = y + 1
        z1 = z + 1
        return [
            self._faces[x1 + z1 * 3] if y == +1 else 0,
            self._faces[9 + z1 + (2 - y1) * 3] if x == -1 else 0,
            self._faces[18 + x1 + (2 - y1) * 3] if z == +1 else 0,
            self._faces[27 + (2 - z1) + (2 - y1) * 3] if x == +1 else 0,
            self._faces[36 + x1 + (2 - y1) * 3] if z == -1 else 0,
            self._faces[45 + x1 + (2 - z1) * 3] if y == -1 else 0]

    def dump(self):
        """ Dumps the current state of the Rubik's cube to stdout. """
        for row in range(3):
            print('       {}'.format(' '.join(str(i) for i in self._faces[row * 3:3 + row * 3])))
        for row in range(3):
            print('{}  {}  {}  {}'.format(
                ' '.join(str(i) for i in self._faces[9 + row * 3:12 + row * 3]),
                ' '.join(str(i) for i in self._faces[18 + row * 3:21 + row * 3]),
                ' '.join(str(i) for i in self._faces[27 + row * 3:30 + row * 3]),
                ' '.join(str(i) for i in self._faces[36 + row * 3:39 + row * 3][::-1])))
        for row in range(3):
            print('       {}'.format(' '.join(str(i) for i in self._faces[45 + row * 3:48 + row * 3])))

    def shuffle(self, count=10, speed=Speed.Fast):
        """ Creates a random cube notation sequence and performs it on the Rubik's cube """
        commands = ' '.join('{}{}'.format(
            random.choice('ULFRBDMES'),
            'i' if random.randrange(5) == 0 else '') for _ in range(count))

        return commands.strip()
