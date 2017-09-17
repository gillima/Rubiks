import logging
import threading
from queue import Queue

from pyglet import clock

from cube.shape import Piece


class RubiksCube(object):
    def __init__(self):
        self.pieces = list(Piece(x - 1, y - 1, z - 1)
                           for x in range(3) for y in range(3) for z in range(3)
                           if x != 1 or y != 1 or z != 1)
        self._commands = Queue()
        self._idle_event = threading.Event()
        clock.schedule_interval(self.tick, interval=0.01)

    def __getitem__(self, item):
        return [p for p in self.pieces if p == item][0]

    def draw(self):
        for piece in self.pieces:
            piece.draw()

    def do(self, commands, speed=5):
        logging.debug('do moves with cube: %s', commands)
        self._idle_event.clear()
        for command in commands.split(' '):
            self._commands.put((command, speed))
        self._idle_event.wait()

    def tick(self, ts, *args, **kwargs):
        if not self._commands.empty() and all(not piece.moving for piece in self.pieces):
            command, speed = self._commands.get()
            for cube in self.pieces:
                cube.rotate(command, speed)

        for cube in self.pieces:
            cube.tick(*args, **kwargs)

        if self._commands.empty() and not self._idle_event.is_set() and not any(p.moving for p in self.pieces):
                self._idle_event.set()

    def face(self, face):
        axis = Piece.Moves[face]['axis']
        expected = Piece.Moves[face]['filter'][axis]
        face_info = Piece.Moves[face]['face']

        pieces = []
        coord = [expected, expected, expected]
        for j in range(-1, 2):
            for i in range(-1, 2):
                coord[abs(face_info[1]) - 1] = i if face_info[1] > 0 else 0 - i
                coord[abs(face_info[2]) - 1] = j if face_info[2] > 0 else 0 - j
                pieces.append(self[tuple(coord)])

        return [p.faces[face_info[0]] for p in pieces]