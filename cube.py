#!/usr/bin/env python3
import sys
from enum import Enum

from pyglet.gl import *
from pyglet.window import key
from pyglet.window.key import symbol_string

from rubiks import CubeView, Cube, Moves, Speed, History


Macros = {
    key.F1: "U R U' R' U' F' U F",  # solve middle layer (to right)
    key.F2: "U' L' U L U F U' F'",  # solve middle layer (to left)
    key.F3: "R U R' U R U U R'",  # solve top layer
    key.F4: "R B' R F F R' B R F F R R",  # position the yellow corners
    key.F5: "R U' R U R U R U' R' U' R R",
    key.F6: "R U R' U'",
    key.F7: "L' U' L U",
}


class InputMode(Enum):
    Direct = 0
    Command = 1


class CubeController(object):
    def __init__(self, cube=None):
        self.cube = cube or Cube()
        self.history = History(self.cube)
        self.on_command_changed = []
        self._input_mode = InputMode.Direct
        self._command = ''

    def on_key_press(self, symbol, modifiers):
        if self._input_mode == InputMode.Direct:
            if symbol == key.COLON:
                self._input_mode = InputMode.Command
                self._set_command(':')
            else:
                self._direct_mode(symbol, modifiers)

        elif self._input_mode == InputMode.Command:
            self._command_mode(symbol, modifiers)

    def _set_command(self, command):
        if command == '':
            self._input_mode = InputMode.Direct
        self._command = command
        for hook in self.on_command_changed:
            hook(self, self._command)

    def _direct_mode(self, symbol, modifiers):
        if symbol_string(symbol) in Moves.keys():
            command = symbol_string(symbol)
            commands = self.cube.create_commands(command)
            self._execute(commands, invert=modifiers & key.MOD_SHIFT, history=True, speed=Speed.Medium)
            self._command = ''

        elif symbol in Macros.keys():
            commands = self.cube.create_commands(Macros[symbol])
            self._execute(commands, invert=modifiers & key.MOD_SHIFT, history=True, speed=Speed.Medium)
            self._command = ''

    def _command_mode(self, symbol, modifiers):
        if symbol_string(symbol) in Moves.keys():
            command = symbol_string(symbol)
            if modifiers & key.MOD_SHIFT:
                command += "'"
            self._set_command(' '.join([self._command, command]))

        if symbol == key.EXCLAMATION:
            self._set_command(self._command + '!')
        elif symbol == key.ASTERISK:
            self._set_command(self._command + 'shuffle')
        elif symbol == key.BACKSPACE:
            self._set_command(self._command[:-1])
        elif symbol in range(key._0, key._9 + 1):
            self._set_command(self._command + str(symbol - key._0))
        elif symbol == key.Q:
            self._set_command(self._command + 'quit')

        elif symbol == key.ENTER:
            command = self._command[1:]  # strip colon
            invert = command[0] == '!'
            if invert:
                command = command[1:]  # strip invert

            # execute commands
            if command == 'shuffle':
                sequence = self.cube.shuffle(count=10)
                commands = self.cube.create_commands(sequence)
                self._execute(commands=commands, history=True, speed=Speed.Fast)

            elif command == 'quit':
                sys.exit(0)

            elif command.isnumeric():
                index = int(command) - 1
                commands, speed = self.history.get(index)
                if commands:
                    self._execute(commands=commands, invert=invert, history=True, speed=speed)

            else:
                try:
                    commands = self.cube.create_commands(command)
                    self._execute(commands=commands, history=True, speed=Speed.Medium)
                except KeyError:
                    print('Unable to create command: {}'.format(self._command))

            # back to direct mode
            self._set_command('')

    def _execute(self, commands, invert=False, history=True, speed=Speed.Medium):
        if invert:
            commands = [c.invert() for c in commands[::-1]]
        if history:
            self.history.append(commands, speed=speed)
        for command in commands:
            command(speed=speed)


if __name__ == '__main__':
    controller = CubeController()

    window = pyglet.window.Window(width=1024, height=768, caption="The Rubik's Cube", resizable=True)
    window.push_handlers(controller.on_key_press)
    view = CubeView(controller, window)

    pyglet.app.run()
