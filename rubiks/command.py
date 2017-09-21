import threading
from itertools import chain
from queue import Queue

from rubiks.config import Moves, Speed


class CommandQueue(object):
    def __init__(self):
        self._queue = Queue()
        self._thread = None
        self._stop_event = threading.Event()

    def __enter__(self):
        self._thread = threading.Thread(target=self._process_commands)
        self._thread.daemon = True
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        self._thread.join()

    def __call__(self, command, *args, **kwargs):
        entry = (command, args, kwargs)
        self._queue.put(entry)

    def _process_commands(self):
        while not self._stop_event.is_set():
            try:
                command, args, kwargs = self._queue.get(timeout=200)
                command(*args, **kwargs)
            except TimeoutError:
                pass


DefaultQueue = CommandQueue()
DefaultQueue.__enter__()


class Command(object):
    """
    Encapsulates a Rubik's cube command and provides printing in cube notation.
    The command will automatically be scheduled on the command queue for execution to ensure the command
    is executed 'non-blocking'.
    """
    def __init__(self, cube, command, queue=DefaultQueue):
        self._cube = cube
        self._command = command[0]
        self._inverse = False
        self._count = 1
        self._queue = queue

        command = command[1:]
        if command and command[0] in "i'":
            self._inverse = True
            command = command[1:]
        if command.isdigit():
            self._count = int(command)
        if self._count % 2 == 0:
            self._inverse = False

    def __call__(self, *args, **kwargs):
        self._queue(self.execute, *args, **kwargs)

    def __str__(self):
        return '{}{}{}'.format(
            self._command,
            '' if not self._inverse else "'",
            '' if self._count == 1 else self._count)

    def execute(self, *args, **kwargs):
        speed = kwargs.get('speed', Speed.Medium)
        inverse = kwargs.get('inverse')
        inverse = self._inverse if not inverse else not self._inverse

        spec = Moves[self._command]
        for _ in range(self._count):
            for face in spec['face']:
                self._apply_indices([[i + abs(face) * 9 for i in [0, 3, 6, 7, 8, 5, 2, 1]]],
                                    inverse if face >= 0 else not inverse, 2)
            self._apply_indices(spec['indices'], inverse, 3)
            self._cube.update(command=self._command, front=spec['face'], inverse=inverse, speed=speed)

    def _apply_indices(self, indices_list, inverse, offset):
        source = list(chain.from_iterable(self._cube._faces))
        for indices in indices_list:
            for i in range(len(indices)):
                i_from = indices[(i + offset) % len(indices)]
                i_to = indices[i]
                if inverse:
                    i_from, i_to = i_to, i_from
                self._cube._faces[i_to // 9][i_to % 9] = source[i_from]


