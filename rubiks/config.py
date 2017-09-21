from enum import Enum


# Animation speed for 3D cube
class Speed(Enum):
    Slow = 5
    Medium = 15
    Fast = 30
    Immediate = 90


# Side length of the cube
CubeSize = 90
PieceScale = .9

# Configuration used for 3D drawing
Faces = [[2, 6, 7, 3], [0, 2, 3, 1], [0, 4, 6, 2], [4, 5, 7, 6], [5, 1, 3, 7], [0, 1, 5, 4]]
Vertices = [-1, -1, 1, -1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1]
Colors = [[50, 50, 50], [255, 255, 255], [0, 128, 0], [255, 0, 0], [0, 0, 255], [255, 144, 0], [255, 255, 0]]

# Axis, front face and rotation direction for animation
Animation = {
    'L': {'axis': 0, 'face': -1, 'dir': -1},
    'M': {'axis': 0, 'face': 0, 'dir': -1},
    'R': {'axis': 0, 'face': +1, 'dir': +1},
    'X': {'axis': 0, 'face': None, 'dir': -1},
    'U': {'axis': 1, 'face': +1, 'dir': +1},
    'E': {'axis': 1, 'face': 0, 'dir': +1},
    'D': {'axis': 1, 'face': -1, 'dir': -1},
    'Y': {'axis': 1, 'face': None, 'dir': +1},
    'F': {'axis': 2, 'face': +1, 'dir': +1},
    'S': {'axis': 2, 'face': 0, 'dir': +1},
    'B': {'axis': 2, 'face': -1, 'dir': -1},
    'Z': {'axis': 2, 'face': None, 'dir': +1},
}

# Front face and piece-face index for textual moves
Moves = {
    'L': dict(face=[1], indices=[[36, 39, 42, 51, 48, 45, 24, 21, 18, 6, 3, 0]]),
    'M': dict(face=[], indices=[[37, 40, 43, 52, 49, 46, 25, 22, 19, 7, 4, 1]]),
    'R': dict(face=[3], indices=[[2, 5, 8, 20, 23, 26, 47, 50, 53, 44, 41, 38]]),
    'X': dict(face=[1, -3], indices=[
        [36, 39, 42, 51, 48, 45, 24, 21, 18, 6, 3, 0],
        [37, 40, 43, 52, 49, 46, 25, 22, 19, 7, 4, 1],
        [38, 41, 44, 53, 50, 47, 26, 23, 20, 8, 5, 2],
    ]),
    'U': dict(face=[0], indices=[[9, 10, 11, 18, 19, 20, 27, 28, 29, 38, 37, 36]]),
    'E': dict(face=[], indices=[[12, 13, 14, 21, 22, 23, 30, 31, 32, 41, 40, 39]]),
    'D': dict(face=[5], indices=[[42, 43, 44, 35, 34, 33, 26, 25, 24, 17, 16, 15]]),
    'Z': dict(face=[2, 4], indices=[
        [11, 14, 17, 45, 46, 47, 33, 30, 27, 8, 7, 6],
        [3, 4, 5, 28, 31, 34, 50, 49, 48, 16, 13, 10],
        [9, 12, 15, 51, 52, 53, 35, 32, 29, 2, 1, 0]
    ]),
    'F': dict(face=[2], indices=[[11, 14, 17, 45, 46, 47, 33, 30, 27, 8, 7, 6]]),
    'S': dict(face=[], indices=[[10, 13, 16, 48, 49, 50, 34, 31, 28, 5, 4, 3]]),
    'B': dict(face=[-4], indices=[[0, 1, 2, 29, 32, 35, 53, 52, 51, 15, 12, 9]]),
    'Y': dict(face=[0, -5], indices=[
        [9, 10, 11, 18, 19, 20, 27, 28, 29, 38, 37, 36],
        [12, 13, 14, 21, 22, 23, 30, 31, 32, 41, 40, 39],
        [15, 16, 17, 24, 25, 26, 33, 34, 35, 44, 43, 42]
    ]),
}
