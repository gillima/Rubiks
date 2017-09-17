import logging
import threading
from queue import Queue

from pyglet import clock

from cube.shape import Piece


class RubiksCube(object):
    def __init__(self):
        self.pieces = {(x, y, z): Piece(x, y, z)
                       for x in range(-1,2) for y in range(-1,2) for z in range(-1,2)
                       if x or y or z}
        self._moving = []

        self._commands = Queue()
        self._idle_event = threading.Event()
        clock.schedule_interval(self.tick, interval=0.01)

    def __getitem__(self, item):
        return self.pieces[item]

    def draw(self):
        for piece in self.pieces.values():
            piece.draw()

    def do(self, commands, speed=5):
        logging.debug('do moves with cube: %s', commands)
        self._idle_event.clear()
        for command in commands.split(' '):
            self._commands.put((command, speed))
        self._idle_event.wait()

    def tick(self, ts, *args, **kwargs):
        if not self._moving and not self._commands.empty():
            command, speed = self._commands.get()
            self._moving = [cube for cube in self.pieces.values() if cube.rotate(command, speed)]

        for cube in self.pieces.values():
            if cube.tick(*args, **kwargs):
                self._moving.remove(cube)
                if self._commands.empty() and not self._idle_event.is_set() and not self._moving:
                    self._idle_event.set()

        if not self._moving:
            self.pieces = {cube.position: cube for cube in self.pieces.values()}

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