#!/usr/bin/env python3
import sys

from pyglet.gl import *
from pyglet.window import key
from pyglet.window.key import symbol_string

from rubiks import Cube, Cube3D, Speed, Cube2D, History
from rubiks.config import Macros, Moves, Background


class CubeWindow(object):
    def __init__(self):
        self._cube = Cube()
        self._cube2d = Cube2D(self._cube)
        self._cube3d = Cube3D(self._cube)
        self._history = History()
        self._view_x = 30
        self._view_y = -30

        self._ratio = 768 / 1024
        self._window = pyglet.window.Window(width=1024, height=768, caption="The Rubik's Cube", resizable=True)
        self._window.push_handlers(
            self.on_draw,
            self.on_key_press,
            self.on_resize)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._draw_2d_cube()
        self._draw_3d_cube()

    def on_resize(self, width, height):
        glClearColor(*Background)
        glShadeModel(GL_SMOOTH)
        glViewport(0, 0, width, height)
        self._cube3d.resize()

    def on_key_press(self, symbol, modifiers):
        if symbol in [key.Q, key.ESCAPE]:
            sys.exit(0)

        elif symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            self._view_x += -15 if symbol == key.UP else 15 if symbol == key.DOWN else 0
            self._view_y += -15 if symbol == key.LEFT else 15 if symbol == key.RIGHT else 0

        elif symbol == key.HOME:
            self._view_x = 30
            self._view_y = -30

        elif symbol in [key.ASTERISK, key.NUM_MULTIPLY]:
            commands = self._cube3d.create_commands(
                self._cube.shuffle(count=10))

            self._history.append(commands, speed=Speed.Fast)
            for command in commands:
                command(speed=Speed.Fast)
            pass

        elif symbol in Macros.keys():
            commands = list(self._cube3d.create_commands(Macros[symbol]))
            inverted = modifiers & key.MOD_SHIFT
            if inverted:
                commands.reverse()

            self._history.append(commands, inverse=inverted, speed=Speed.Medium)
            for command in commands:
                command(inverse=inverted, speed=Speed.Medium)

        elif symbol_string(symbol) in Moves.keys():
            command = symbol_string(symbol)
            if modifiers & key.MOD_SHIFT:
                command += 'i'

            commands = self._cube3d.create_commands(command)
            self._history.append(commands, speed=Speed.Medium)
            for command in commands:
                command(speed=Speed.Medium)

    def _draw_2d_cube(self):
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self._window.width / 2., self._window.width / 2.,
                -self._window.height / 2., self._window.height / 2.,
                0, 8192)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(-self._window.width / 2, self._window.height // 2, 0)

        # draw the 2D cube
        glTranslatef(0, 0, 0)
        self._cube2d.draw()
        self._history.draw()

    def _draw_3d_cube(self):
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, self._window.width / self._window.height, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # draw the 3d cube
        glPushMatrix()
        glTranslatef(50, -20, -400)
        glRotatef(self._view_x, 1, 0, 0)
        glRotatef(self._view_y, 0, 1, 0)
        self._cube3d.draw()
        glPopMatrix()


if __name__ == '__main__':
    window = CubeWindow()
    pyglet.app.run()
