import sys

from pyglet.gl import *
from pyglet.window import key
from pyglet.window.key import symbol_string

from rubiks import Cube3D, Speed
from rubiks.config import Macros, Moves

cube = Cube3D()
keys = key.KeyStateHandler()
view_x = 30
view_y = -30


def _on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glTranslatef(0, 0, -400)
    glRotatef(view_x, 1, 0, 0)
    glRotatef(view_y, 0, 1, 0)
    cube.draw()
    glPopMatrix()


def _on_key_press(symbol, modifiers):
    global view_x, view_y

    if symbol in [key.Q, key.ESCAPE]:
        sys.exit(0)

    elif symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
        view_x += -15 if symbol == key.UP else 15 if symbol == key.DOWN else 0
        view_y += -15 if symbol == key.LEFT else 15 if symbol == key.RIGHT else 0

    elif symbol == key.HOME:
        view_x = 30
        view_y = -30

    elif symbol in [key.ASTERISK, key.NUM_MULTIPLY]:
        cube.shuffle(count=10, speed=Speed.Fast)
        pass

    elif symbol in Macros.keys():
        commands = list(cube.create_commands(Macros[symbol]))
        inverted = modifiers & key.MOD_SHIFT
        if inverted:
            commands.reverse()
        for command in commands:
            command(inverse=inverted, speed=Speed.Medium)

    elif symbol_string(symbol) in Moves.keys():
        command = symbol_string(symbol)
        if modifiers & key.MOD_SHIFT:
            command += 'i'
        cube.do(command, speed=Speed.Medium)


def _on_resize(width, height):
    glViewport(0, 0, width, height)
    glClearColor(0, 0, 0, 0.2)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    gluPerspective(35, width / height, 1, 1000)


if __name__ == '__main__':
    window = pyglet.window.Window(width=480, height=450, caption="The Rubik's Cube", resizable=True)
    window.on_draw = _on_draw
    window.on_resize = _on_resize
    window.on_key_press = _on_key_press
    pyglet.app.run()
