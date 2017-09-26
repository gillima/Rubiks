#!/usr/bin/env python3
from pyglet.gl import *
from rubiks import CubeController, CubeView


if __name__ == '__main__':
    controller = CubeController()

    window = pyglet.window.Window(width=1024, height=768, caption="The Rubik's Cube", resizable=True)
    window.push_handlers(controller.on_key_press)
    view = CubeView(controller, window)

    pyglet.app.run()
