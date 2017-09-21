import threading
from queue import Queue

import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window.key import symbol_string

from .shape import Piece
from .rubiks_cube import RubiksCube
from .utils import shuffle, print_2d


class CubeWindow(object):
    def __init__(self, width, height, caption='Rubik\'s Cube'):
        self._cube = RubiksCube()
        self._keyboard_buffer = Queue()
        self._stop_event = threading.Event()
        keyboard_thread = threading.Thread(target=self._process_keyboard)
        keyboard_thread.daemon = True
        keyboard_thread.start()

        self._window = pyglet.window.Window(width=width, height=height, caption=caption, resizable=True)
        self._window.on_draw = self._on_draw
        self._window.on_resize = self._on_resize
        self._window.on_key_press = self._on_key_press

        self._view_x = 30
        self._view_y = -30

    def _on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(0, 0, -400)
        glRotatef(self._view_x, 1, 0, 0)
        glRotatef(self._view_y, 0, 1, 0)

        self._cube.draw()

    def _on_resize(self, width, height):
        glClearColor(0, 0, 0, 0.2)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self._window.width, self._window.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, width / height, 1, 1000)

    def _on_key_press(self, symbol, modifiers):
        if symbol in [key.Q, key.ESCAPE]:
            self._stop_event.set()
            exit(0)

        elif symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            self._view_x += -15 if symbol == key.UP else 15 if symbol == key.DOWN else 0
            self._view_y += -15 if symbol == key.LEFT else 15 if symbol == key.RIGHT else 0

        elif symbol in [key.HOME]:
            self._view_x = 30
            self._view_y = -30

        else:
            self._keyboard_buffer.put((symbol, modifiers))

    def _process_keyboard(self):
        macros = {
            key._1: "R U R' U'",
            key._2: "L' U' L U",
            key._3: "U R U' R' U' F' U F",  # place edge of middle layer to the right
            key._4: "U' F' U F U R U' R'",  # place edge of middle layer to the left
            key._5: "R U R' U' " + "L' U' L U " + ("R U R' U' " * 5) + ("L' U' L U " * 5),  # non edge destroying rotation of last layer middle pieces
            key._6: "R U R' U R U U R'",  # rotate middle pieces of last layer counter-clock wise
            key._7: "U R U' L' U R' U' L",  # exchange top layed edges counter-clock wise
        }

        while not self._stop_event.is_set():
            try:
                symbol, modifiers = self._keyboard_buffer.get(timeout=100)

                if symbol_string(symbol) in macros.keys():
                    self._cube.do(macros[symbol_string(symbol)], speed=30)

                elif symbol_string(symbol) in Piece.Moves.keys():
                    command = symbol_string(symbol)
                    if modifiers & key.MOD_SHIFT:
                        command += '\''
                    self._cube.do(command, speed=10)

                elif symbol in [key.S]:
                    shuffle(self._cube, count=10, speed=30)

                elif symbol == key.P:
                    print_2d(self._cube)

            except TimeoutError:
                pass

    def run(self):
        pyglet.app.run()
