import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window.key import symbol_string

from cube.shape import RubiksCube


class CubeWindow(object):
    def __init__(self, width, height, caption=''):
        self._cube = RubiksCube()

        self._window = pyglet.window.Window(width=width, height=height,
                                            caption=caption, resizable=True)
        self._window.on_draw = self._on_draw
        self._window.on_resize = self._on_resize
        self._window.on_key_press = self._on_key_press

        self._view_x = 30
        self._view_y = -30

    def _draw_3d_cube(self):
        self._cube.draw()

    def _on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -400)
        glRotatef(self._view_x, 1, 0, 0)
        glRotatef(self._view_y, 0, 1, 0)

        self._draw_3d_cube()

    def _on_resize(self, width, height):
        glClearColor(.1, .1, .1, 1)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self._window.width, self._window.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, width / height, 1, 1000)

    def _on_key_press(self, symbol, modifiers):
        if symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            self._view_x += -15 if symbol == key.UP else 15 if symbol == key.DOWN else 0
            self._view_y += -15 if symbol == key.LEFT else 15 if symbol == key.RIGHT else 0

        elif symbol_string(symbol) in self._cube.moves:
            command = symbol_string(symbol)
            if modifiers & key.MOD_SHIFT:
                command += '\''
            self._cube.do(command)

        elif symbol in [key.HOME]:
            self._view_x = 30
            self._view_y = -30

        elif symbol in [key.S]:
            self._cube.shuffle()

        elif symbol in [key.Q, key.ESCAPE]:
            exit(0)


if __name__ == '__main__':
    window = CubeWindow(width=480, height=400, caption='Cube')
    pyglet.app.run()
