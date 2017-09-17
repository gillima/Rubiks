import random

from cube.shape import Piece, Modifiers


def shuffle(cube, count=10, speed=30):
    command = ''
    for _ in range(count):
        move = random.choice([m for m in Piece.Moves.keys() if m not in 'XYZ'])
        modifier = random.choice(Modifiers)
        command += '{}{} '.format(move, modifier.strip())
    cube.do(command.strip(), speed=speed)


def fitness(cube):
    def face_fitness(face):
        face = cube.face(face)
        return len([s for s in face if s == face[4]])

    return sum(face_fitness(f) for f in 'ULFRBD')


def print_2d(cube):
    u = ''.join(cube.face('U'))
    l = ''.join(cube.face('L'))
    f = ''.join(cube.face('F'))
    r = ''.join(cube.face('R'))
    b = ''.join(cube.face('B'))
    d = ''.join(cube.face('D'))

    print('    {}\n    {}\n    {}\n{} {} {} {}\n{} {} {} {}\n{} {} {} {}\n    {}\n    {}\n    {}\n'.format(
        u[0:3], u[3:6], u[6:9],
        l[0:3], f[0:3], r[0:3], b[0:3],
        l[3:6], f[3:6], r[3:6], b[3:6],
        l[6:9], f[6:9], r[6:9], b[6:9],
        d[0:3], d[3:6], d[6:9]))
    print('fitness: {}'.format(fitness(cube)))
