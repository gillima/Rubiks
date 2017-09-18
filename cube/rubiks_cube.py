import logging
import threading
from queue import Queue

from pyglet import clock

from cube.shape import Piece


class RubiksCube(object):
    def __init__(self):
        self.pieces = {(x, y, z): Piece(x, y, z)
                       for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)
                       if x or y or z}
        self._moving = []
        self._commands = []
        self._idle_event = threading.Event()

    def __getitem__(self, item):
        return self.pieces[item]

    def draw(self):
        for piece in self.pieces.values():
            piece.draw()

    def do(self, commands, speed):
        logging.debug('do moves with cube: %s', commands)
        self._idle_event.clear()
        for command in commands.split(' '):
            self._commands.append((command, speed))
        clock.schedule_interval(self.tick, interval=0.01)
        self._idle_event.wait()
        clock.unschedule(self.tick)

    def tick(self, ts, *args, **kwargs):
        if not self._moving and self._commands:
            command, speed = self._commands.pop(0)
            self._moving = [cube for cube in self.pieces.values() if cube.rotate(command, speed)]

        for cube in self.pieces.values():
            if cube.tick(*args, **kwargs):
                self._moving.remove(cube)

        if not self._moving:
            self.pieces = {cube.position: cube for cube in self.pieces.values()}
            if not self._idle_event.is_set() and not self._commands:
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
