from .config import Speed


class History(object):
    def __init__(self):
        self._commands = []

    def append(self, commands, **kwargs):
        inverse = kwargs.get('inverse', False)
        speed = kwargs.get('speed', Speed.Medium)
        command = ' '.join([c.to_string(inverse=inverse) for c in commands])
        self._commands.append((command, speed))

    def draw(self):
        pass
