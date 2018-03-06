from random import randint


class Data:

    points = []
    neighbouring_points = []
    def __init__(self, initial_conditions, update_rule, side):
        self.side = side
        self.update_rule = update_rule
        for i in xrange(2000):
            Data.points.append(initial_conditions())

    def move(self):
        for i, point in enumerate(Data.points):
            Data.points[i] = self.update_rule(*point)

    def update_neighbours(self, spatial_hash_map, cartesian_coords):
        x, y, z = cartesian_coords
        bb = [
            int(x) - self.side, int(y) - self.side, int(z) - self.side,
            int(x) + self.side, int(y) + self.side, int(z) + self.side
        ]
        Data.neighbouring_points = spatial_hash_map.get_local_points(bb)
