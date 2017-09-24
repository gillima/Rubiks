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

    def append(self, commands, **kwargs):
        inverse = kwargs.get('inverse', False)
        speed = kwargs.get('speed', Speed.Medium)
        command = ' '.join([c.to_string(inverse=inverse) for c in commands])
        self._commands.append((command, speed))
        self._update()

    def resize(self, width, height):
        self._height = height
        self._update()

    def _update(self):
        self._layout.begin_update()
        self._document.text = '\n'.join(str(c[0]) for c in self._commands)
        self._document.set_style(0,len(self._document.text),dict(color=(255,255,255,255)))

        if self._document.text:
            self._layout.height = self._height - 30
            self._layout.y = 0
        self._layout.view_y = -self._layout.content_height
        self._layout.end_update()


    def draw(self):
        self._batch.draw()
