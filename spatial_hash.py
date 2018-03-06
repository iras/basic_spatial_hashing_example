class SpatialHashMap:

    def __init__(self, power_of_two_bin_size):
        self.shift = power_of_two_bin_size
        self.bins = {}

    def _get_hash(self, x, y, z):
        return x >> self.shift, y >> self.shift, z >> self.shift

    def insert(self, point):
        key = self._get_hash(*point)
        if key not in self.bins:
            self.bins[key] = []
        self.bins[key].append(point)

    def get_local_points(self, bounding_box):
        min_x, min_y, min_z, max_x, max_y, max_z = bounding_box
        min_hash_x, min_hash_y, min_hash_z = self._get_hash(min_x, min_y, min_z)
        max_hash_x, max_hash_y, max_hash_z = self._get_hash(max_x, max_y, max_z)

        local_points = []
        for hash_x in xrange(min_hash_x, max_hash_x + 1):
            for hash_y in xrange(min_hash_y, max_hash_y + 1):
                for hash_z in xrange(min_hash_z, max_hash_z + 1):
                    if (hash_x, hash_y, hash_z) in self.bins:
                        local_points.extend(self.bins[(hash_x, hash_y, hash_z)])

        return local_points

    def restart(self):
        self.bins = {}

    def generate(self, points):
        for point in points:
            self.insert(point)
