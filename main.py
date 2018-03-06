#!/usr/local/bin/python
from spatial_hash import SpatialHashMap
from random import randint
from canvas import Canvas
from data import Data

power_of_two = 3

def initial_conditions():
    return (randint(-100, 100), randint(-100, 100), 0,)

def update_rule(x, y, z):
    return (x + randint(-1, 1), y + randint(-1, 1), z,)

d = Data(initial_conditions, update_rule, int(2 ** power_of_two))

s = SpatialHashMap(power_of_two)
s.generate(d.points)

def external_funct(cartesian_coords):
    d.move()

    s.restart()
    for point in d.points:
        s.insert(point)

    d.update_neighbours(s, cartesian_coords)

a = Canvas(512, external_funct, d)
