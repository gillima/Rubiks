#!/usr/bin/env python3
import sys

from pyglet.gl import *
from pyglet.window import key
from pyglet.window.key import symbol_string

from rubiks import Cube3D, Speed
from rubiks.config import Macros, Moves, Background


class CubeWindow(object):
    def __init__(self):
        self._cube = Cube3D()
        self._view_x = 30
        self._view_y = -30

        self._window = pyglet.window.Window(width=480, height=450, caption="The Rubik's Cube", resizable=True)
        self._window.on_draw = self._on_draw
        self._window.on_resize = self._on_resize
        self._window.on_key_press = self._on_key_press

    def _on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPushMatrix()
        glTranslatef(0, 0, -400)
        glRotatef(self._view_x, 1, 0, 0)
        glRotatef(self._view_y, 0, 1, 0)
        self._cube.draw()
        glPopMatrix()

    def _on_key_press(self, symbol, modifiers):
        if symbol in [key.Q, key.ESCAPE]:
            sys.exit(0)

        elif symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            self._view_x += -15 if symbol == key.UP else 15 if symbol == key.DOWN else 0
            self._view_y += -15 if symbol == key.LEFT else 15 if symbol == key.RIGHT else 0

        elif symbol == key.HOME:
            self._view_x = 30
            self._view_y = -30

        elif symbol in [key.ASTERISK, key.NUM_MULTIPLY]:
            self._cube.shuffle(count=10, speed=Speed.Fast)
            pass

        elif symbol in Macros.keys():
            commands = list(self._cube.create_commands(Macros[symbol]))
            inverted = modifiers & key.MOD_SHIFT
            if inverted:
                commands.reverse()
            for command in commands:
                command(inverse=inverted, speed=Speed.Medium)

        elif symbol_string(symbol) in Moves.keys():
            command = symbol_string(symbol)
            if modifiers & key.MOD_SHIFT:
                command += 'i'
            self._cube.do(command, speed=Speed.Medium)

    def _on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glClearColor(*Background)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        self._cube.resize()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, width / height, 1, 1000)


if __name__ == '__main__':
    window = CubeWindow()
    pyglet.app.run()
