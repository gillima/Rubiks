from cube import CubeWindow
import logging.config


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    window = CubeWindow(width=480, height=400, caption='Cube')
    window.run()
