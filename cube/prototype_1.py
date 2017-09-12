import random
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window.key import symbol_string


class Cube(object):
    Moves = 'FBRLUDHJKXYZ'
    Modifiers = ' \'2'

    def __init__(self):
        self._faces = {
            'U': 'WWWWWWWWW',
            'L': 'GGGGGGGGG',
            'F': 'RRRRRRRRR',
            'R': 'BBBBBBBBB',
            'B': 'OOOOOOOOO',
            'D': 'YYYYYYYYY',
        }

    def rotate(self, rotation_spec):
        specs = rotation_spec.split(' ')
        for spec in specs:
            if not spec[0] in Cube.Moves:
                continue
            count = 1
            if len(spec) > 1 and spec[1] == '2':
                count = 2
            elif len(spec) > 1 and spec[1] == '\'':
                count = 3
            for _ in range(count):
                if spec[0] == 'F':
                    self._front()
                elif spec[0] == 'B':
                    self._back()
                elif spec[0] == 'R':
                    self._right()
                elif spec[0] == 'L':
                    self._left()
                elif spec[0] == 'U':
                    self._upper()
                elif spec[0] == 'D':
                    self._down()
                elif spec[0] == 'X':
                    self._x_middle()
                elif spec[0] == 'Y':
                    self._y_middle()
                elif spec[0] == 'Z':
                    self._z_middle()

                elif spec[0] == 'J':
                    self._rotate_y()
                elif spec[0] == 'K':
                    self._rotate_x()
                elif spec[0] == 'H':
                    self._rotate_z()

    def _front(self):
        f = self._faces
        tmp = f['U'][6:9]
        f['U'] = f['U'][0:6] + f['L'][2::3][::-1]
        f['L'] = f['L'][0:2] + f['D'][0] + f['L'][3:5] + f['D'][1] + f['L'][6:8] + f['D'][2]
        f['D'] = f['R'][0::3][::-1] + f['D'][3:]
        f['R'] = tmp[0] + f['R'][1:3] + tmp[1] + f['R'][4:6] + tmp[2] + f['R'][7:9]
        f['F'] = f['F'][0::3][::-1] + f['F'][1::3][::-1] + f['F'][2::3][::-1]

    def _back(self):
        f = self._faces
        tmp = f['R'][2::3]
        f['R'] = f['R'][0:2] + f['D'][8] + f['R'][3:5] + f['D'][7] + f['R'][6:8] + f['D'][6]
        f['D'] = f['D'][0:6] + f['L'][0::3]
        f['L'] = f['U'][2] + f['L'][1:3] + f['U'][1] + f['L'][4:6] + f['U'][0] + f['L'][7:]
        f['U'] = tmp + f['U'][3:]
        f['B'] = f['B'][0::3][::-1] + f['B'][1::3][::-1] + f['B'][2::3][::-1]

    def _right(self):
        f = self._faces
        tmp = f['F'][2::3]
        f['F'] = f['F'][0:2] + f['D'][2] + f['F'][3:5] + f['D'][5] + f['F'][6:8] + f['D'][8]
        f['D'] = f['D'][0:2] + f['B'][6] + f['D'][3:5] + f['B'][3] + f['D'][6:8] + f['B'][0]
        f['B'] = f['U'][8] + f['B'][1:3] + f['U'][5] + f['B'][4:6] + f['U'][2] + f['B'][7:9]
        f['U'] = f['U'][0:2] + tmp[0] + f['U'][3:5] + tmp[1] + f['U'][6:8] + tmp[2]
        f['R'] = f['R'][0::3][::-1] + f['R'][1::3][::-1] + f['R'][2::3][::-1]

    def _left(self):
        f = self._faces
        tmp = f['D'][0::3]
        f['D'] = f['F'][0] + f['D'][1:3] + f['F'][3] + f['D'][4:6] + f['F'][6] + f['D'][7:9]
        f['F'] = f['U'][0] + f['F'][1:3] + f['U'][3] + f['F'][4:6] + f['U'][6] + f['F'][7:9]
        f['U'] = f['B'][8] + f['U'][1:3] + f['B'][5] + f['U'][4:6] + f['B'][2] + f['U'][7:9]
        f['B'] = f['B'][0:2] + tmp[2] + f['B'][3:5] + tmp[1] + f['B'][6:8] + tmp[0]
        f['L'] = f['L'][0::3][::-1] + f['L'][1::3][::-1] + f['L'][2::3][::-1]

    def _upper(self):
        f = self._faces
        tmp = f['L'][0:3]
        f['L'] = f['F'][0:3] + f['L'][3:]
        f['F'] = f['R'][0:3] + f['F'][3:]
        f['R'] = f['B'][0:3] + f['R'][3:]
        f['B'] = tmp + f['B'][3:]
        f['U'] = f['U'][0::3][::-1] + f['U'][1::3][::-1] + f['U'][2::3][::-1]

    def _down(self):
        f = self._faces
        tmp = f['B'][6:]
        f['B'] = f['B'][0:6] + f['R'][6:]
        f['R'] = f['R'][0:6] + f['F'][6:]
        f['F'] = f['F'][0:6] + f['L'][6:]
        f['L'] = f['L'][0:6] + tmp
        f['D'] = f['D'][0::3][::-1] + f['D'][1::3][::-1] + f['D'][2::3][::-1]

    def _x_middle(self):
        f = self._faces
        tmp = f['F'][1::3]
        f['F'] = f['F'][0] + f['D'][1] + f['F'][2] + f['F'][3] + f['D'][4] + f['F'][5] + f['F'][6] + f['D'][7] + f['F'][8]
        f['D'] = f['D'][0] + f['B'][7] + f['D'][2] + f['D'][3] + f['B'][4] + f['D'][5] + f['D'][6] + f['B'][1] + f['D'][8]
        f['B'] = f['B'][0] + f['U'][7] + f['B'][2] + f['B'][3] + f['U'][4] + f['B'][5] + f['B'][6] + f['U'][1] + f['B'][8]
        f['U'] = f['U'][0] + tmp[0] + f['U'][2] + f['U'][3] + tmp[1] + f['U'][5] + f['U'][6] + tmp[2] + f['U'][8]

    def _y_middle(self):
        f = self._faces
        tmp = f['F'][3:6]
        f['F'] = f['F'][0:3] + f['R'][3:6] + f['F'][6:9]
        f['R'] = f['R'][0:3] + f['B'][3:6] + f['R'][6:9]
        f['B'] = f['B'][0:3] + f['L'][3:6] + f['B'][6:9]
        f['L'] = f['L'][0:3] + tmp + f['L'][6:9]

    def _z_middle(self):
        f = self._faces
        tmp = f['U'][3:6]
        f['U'] = f['U'][0:3] + f['L'][1::3][::-1] + f['U'][6:9]
        f['L'] = f['L'][0] + f['D'][3] + f['L'][2] + f['L'][3] + f['D'][4] + f['L'][5] + f['L'][6] + f['D'][5] + f['L'][8]
        f['D'] = f['D'][0:3] + f['R'][1::3][::-1] + f['D'][6:9]
        f['R'] = f['R'][0] + tmp[0] + f['R'][2] + f['R'][3] + tmp[1] + f['R'][5] + f['R'][6] + tmp[2] + f['R'][8]

    def _rotate_x(self):
        self._right()
        self._x_middle()
        self._left()
        self._left()
        self._left()

    def _rotate_y(self):
        self._upper()
        self._y_middle()
        self._down()
        self._down()
        self._down()

    def _rotate_z(self):
        self._front()
        self._z_middle()
        self._back()
        self._back()
        self._back()

    def shuffle(self, count=10):
        for _ in range(count):
            move = random.choice(Cube.Moves)
            modifier = random.choice(Cube.Modifiers)
            self.rotate('{}{}'.format(move, modifier).strip())

    def __str__(self):
        return \
            '    {}\n    {}\n    {}\n'.format(self._faces['U'][0:3], self._faces['U'][3:6], self._faces['U'][6:9]) + \
            '{} {} {} {}\n'.format(self._faces['L'][0:3], self._faces['F'][0:3], self._faces['R'][0:3], self._faces['B'][0:3]) + \
            '{} {} {} {}\n'.format(self._faces['L'][3:6], self._faces['F'][3:6], self._faces['R'][3:6], self._faces['B'][3:6]) + \
            '{} {} {} {}\n'.format(self._faces['L'][6:9], self._faces['F'][6:9], self._faces['R'][6:9], self._faces['B'][6:9]) + \
            '    {}\n    {}\n    {}\n'.format(self._faces['D'][0:3], self._faces['D'][3:6], self._faces['D'][6:9])


class CubeWindow(Cube):
    def __init__(self, width, height, title=''):
        super(CubeWindow, self).__init__()
        self._window = pyglet.window.Window(width=width, height=height, caption=title)
        self._window.on_draw = self.on_draw
        self._window.on_key_press = self.on_key_press

        self._size = width / 15
        self._space = self._size / 15
        self._view_x = 30
        self._view_y = 30

        glClearColor(0, 0, 0, 1)

    def _set_color(self, color):
         if color == 'W':
             glColor3ub(255, 255, 255)
         elif color == 'G':
             glColor3ub(0, 128, 0)
         elif color == 'R':
             glColor3ub(255, 0, 0)
         elif color == 'B':
             glColor3ub(0, 0, 255)
         elif color == 'O':
             glColor3ub(255, 165, 0)
         elif color == 'Y':
             glColor3ub(255, 255, 0)

    def _draw_rect(self, x, y, z, orientation, color):
        x -= 1.5
        y -= 1.5
        z -= 1.5
        x *= self._size + self._space
        y *= self._size + self._space
        z *= self._size + self._space
        shift = self._space / 2

        glBegin(GL_QUADS)
        self._set_color(color)

        if orientation in 'UD':
            glVertex3f(x, y - shift, z)
            glVertex3f(x + self._size, y - shift, z)
            glVertex3f(x + self._size, y - shift, z + self._size)
            glVertex3f(x, y - shift, z + self._size)

        elif orientation in 'LR':
            glVertex3f(x - shift, y, z)
            glVertex3f(x - shift, y + self._size, z)
            glVertex3f(x - shift, y + self._size, z + self._size)
            glVertex3f(x - shift, y, z + self._size)

        elif orientation in 'FB':
            glVertex3f(x, y, z - shift)
            glVertex3f(x + self._size, y, z - shift)
            glVertex3f(x + self._size, y + self._size, z - shift)
            glVertex3f(x, y + self._size, z - shift)

        glEnd()

    def _draw_inner_cube(self):
        l = (self._size + self._space * 0.95) * 3 / 2
        s = self._space / 2
        glColor3ub(0, 0, 0)
        glBegin(GL_QUADS)

        glVertex3f(l, l, l - s)
        glVertex3f(l, -l, l - s)
        glVertex3f(-l, -l, l - s)
        glVertex3f(-l, l, l - s)

        glVertex3f(l, l, -l - s)
        glVertex3f(l, -l, -l - s)
        glVertex3f(-l, -l, -l - s)
        glVertex3f(-l, l, -l - s)

        glVertex3f(l - s, l, l)
        glVertex3f(l - s, l, -l)
        glVertex3f(l - s, -l, -l)
        glVertex3f(l - s, -l, l)

        glVertex3f(-l - s, l, l)
        glVertex3f(-l - s, l, -l)
        glVertex3f(-l - s, -l, -l)
        glVertex3f(-l - s, -l, l)

        glVertex3f(l, l - s, l)
        glVertex3f(-l, l - s, l)
        glVertex3f(-l, l - s, -l)
        glVertex3f(l, l - s, -l)

        glVertex3f(l, -l - s, l)
        glVertex3f(-l, -l - s, l)
        glVertex3f(-l, -l - s, -l)
        glVertex3f(l, -l - s, -l)

        glEnd()

    def _draw_3d_cube(self):
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self._window.width, self._window.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, 1, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glTranslatef(0, 0, -400)

        # draw 3D cube
        glPushMatrix()
        glRotatef(self._view_x, 1, 0, 0)
        glRotatef(self._view_y, 0, 1, 0)

        self._draw_inner_cube()
        for index, color in enumerate(self._faces['F']):
            self._draw_rect(index % 3, 2 - index // 3, 3, 'F', color)
        for index, color in enumerate(self._faces['B']):
            self._draw_rect(2 - index % 3, 2 - index // 3, 0, 'B', color)
        for index, color in enumerate(self._faces['L']):
            self._draw_rect(0, 2 - index // 3, index % 3, 'L', color)
        for index, color in enumerate(self._faces['R']):
            self._draw_rect(3, 2 - index // 3, 2 - index % 3, 'R', color)
        for index, color in enumerate(self._faces['U']):
            self._draw_rect(index % 3, 3, index // 3, 'U', color)
        for index, color in enumerate(self._faces['D']):
            self._draw_rect(index % 3, 0, 2 - index // 3, 'D', color)

        glPopMatrix()

    def _draw_2d_cube(self):
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, self._window.height / 6 * 4, self._window.width / 3, self._window.height / 3)
        glOrtho(0, 20, 0, 20, 0, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPushMatrix()
        self._draw_2d_face('U', 3, 6)
        self._draw_2d_face('L', 0, 3)
        self._draw_2d_face('F', 3, 3)
        self._draw_2d_face('R', 6, 3)
        self._draw_2d_face('B', 9, 3)
        self._draw_2d_face('D', 3, 0)
        glPopMatrix()

    def _draw_2d_face(self, face, x_offset, y_offset):
        x_offset += 3
        y_offset += 12
        for index, color in enumerate(self._faces[face]):
            x = (index % 3)
            y = (index // 3)
            self._set_color(color)
            glBegin(GL_QUADS)
            glVertex2f(x_offset + x, y_offset - y)
            glVertex2f(x_offset + x + .9, y_offset - y)
            glVertex2f(x_offset + x + .9, y_offset - y - .9)
            glVertex2f(x_offset + x, y_offset - y - .9)
            glEnd()

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self._draw_3d_cube()
        self._draw_2d_cube()

    def on_key_press(self, symbol, modifiers):
        if symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            self._view_x += -15 if symbol == key.UP else 15 if symbol == key.DOWN else 0
            self._view_y += -15 if symbol == key.LEFT else 15 if symbol == key.RIGHT else 0

        elif symbol_string(symbol) in Cube.Moves:
            command = symbol_string(symbol)
            if modifiers & key.MOD_SHIFT:
                command += '\''
            self.rotate(command)

        elif symbol in [key.HOME]:
            self._view_x = 30
            self._view_y = 30

        elif symbol in [key.S]:
            self.shuffle()

        elif symbol in [key.Q, key.ESCAPE]:
            exit(0)

if __name__ == '__main__':
    cube = CubeWindow(480, 440, 'Cube')
    pyglet.app.run()
