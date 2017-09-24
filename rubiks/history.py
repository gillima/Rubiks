import pyglet
from pyglet.gl import *

from .config import Speed


class History(object):
    def __init__(self, width, height):
        self._commands = []
        self._height = height
        self._batch = pyglet.graphics.Batch()
        self._document = pyglet.text.document.FormattedDocument()
        self._document.text = '\n'
        self._layout = pyglet.text.layout.ScrollableTextLayout(self._document, width, height, multiline=True, batch=self._batch)
        self._update()

    def append(self, commands, speed=Speed.Medium):
        self._commands.append((commands, speed))
        self._update()

    def get(self, index):
        if len(self._commands) < index:
            return None, None
        return self._commands[int(index) - 1]

    def resize(self, width, height):
        self._height = height
        self._update()

    def _update(self):
        self._layout.begin_update()

        text = ''
        for i, commands in enumerate(self._commands):
            if not commands[0]:
                continue
            command = ' '.join(['{}'.format(c) for c in commands[0]])
            text += '{}: {}\n'.format(i + 1, command)

        self._document.text = text
        self._document.set_style(0,len(self._document.text),dict(color=(255,255,255,255)))

        if self._document.text:
            self._layout.height = self._height - 30
            self._layout.y = 0

        self._layout.view_y = -self._layout.content_height
        self._layout.end_update()


    def draw(self):
        self._batch.draw()
