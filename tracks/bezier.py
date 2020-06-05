from enum import Enum

from tracks.vector import Vector


class Rotate(Enum):
    deg_0 = 0
    deg_90 = 1
    deg_180 = 2
    deg_270 = 3


class Track(object):
    def __init__(self, tile: tuple,
                 configuration,
                 rotation,
                 color=(255, 255, 255),
                 handles=False,
                 precision=15,
                 reverse=False):
        self.curve: Bezier = None
        self.tile = tile
        self.type = configuration
        self.rotation = rotation
        self.color = color
        self.precision = precision
        self.show_handles = handles
        self.reverse = reverse

        self._define_curve()
        self.handles = self.curve.keys

    def get_point(self, t):
        return self.curve.get_point(t)

    def _define_curve(self):
        reverse = self.reverse

        def cv(*args):
            pts = list(args)
            if reverse:
                first = pts[0]
                last = pts[-1]
                pts[-1] = first
                pts[0] = last
            return Bezier(*pts, precision=self.precision)

        x, y = self.tile

        a = (x, y)
        b = (x, y + 1)
        c = (x + 1, y + 1)
        d = (x + 1, y)

        if self.type == "angle":
            if self.rotation == Rotate.deg_0:
                self.curve = cv(a, b, c)
            elif self.rotation == Rotate.deg_90:
                self.curve = cv(b, c, d)
            elif self.rotation == Rotate.deg_180:
                self.curve = cv(c, d, a)
            elif self.rotation == Rotate.deg_270:
                self.curve = cv(d, a, b)
        elif self.type == "straight":
            if self.rotation == Rotate.deg_0:
                self.curve = cv(a, b)
            elif self.rotation == Rotate.deg_90:
                self.curve = cv(b, c)
            elif self.rotation == Rotate.deg_180:
                self.curve = cv(c, d)
            elif self.rotation == Rotate.deg_270:
                self.curve = cv(d, a)


class Bezier(object):
    def __init__(self, a: tuple, b: tuple, c: tuple = None, d: tuple = None, precision=20):
        self.keys = []
        self.a = Vector(a[0], a[1])
        self.keys.append(self.a)
        self.b = Vector(b[0], b[1])
        self.keys.append(self.b)
        self.form = "linear"
        self.c = None
        self.d = None
        if c is not None:
            self.form = "square"
            self.c = Vector(c[0], c[1])
            self.keys.append(self.c)
        if d is not None:
            self.form = "cubic"
            self.d = Vector(d[0], d[1])
            self.keys.append(self.d)

        self.length = 0
        self.precision = precision
        self.arc_lengths = []
        self.calculate_arc_length()

    def calculate_arc_length(self):
        timestep = 1.0 / self.precision
        self.arc_lengths.append(0)
        for idx in range(self.precision):
            distance = self._get_point(timestep * idx).distance(self._get_point(timestep * (idx + 1)))
            self.arc_lengths.append(self.arc_lengths[idx] + distance)
        self.length = self.arc_lengths[-1]
        # self.length = 1.0

    def get_point(self, t) -> Vector:
        assert (0.0 <= t <= 1.0)
        if t == 0.0:
            return self._get_point(0.0)
        if t == 1.0:
            return self._get_point(1.0)
        u = t * self.length
        prev = self.arc_lengths[0]
        prev_index = 0
        new_t = -1
        for idx, arc_len in enumerate(self.arc_lengths):
            if (u >= prev) and (u < arc_len):
                segment_fraction = (u - prev) / (arc_len - prev)
                new_t = (prev_index + segment_fraction) / float((len(self.arc_lengths) - 1))
                break
            else:
                prev = arc_len
                prev_index = idx
        assert (new_t >= 0.0)
        return self._get_point(new_t)

    def _get_point(self, t) -> Vector:
        assert (0.0 <= t <= 1.0)
        if self.form == "linear":
            return self._get_point_linear(t)
        elif self.form == "square":
            return self._get_point_square(t)
        elif self.form == "cubic":
            return self._get_point_cubic(t)

    def _get_point_linear(self, t) -> Vector:
        a = self.a.multiply(1 - t)
        b = self.b.multiply(t)
        return a + b

    def _get_point_square(self, t) -> Vector:
        a = self.a.multiply(pow((1 - t), 2))
        b = self.b.multiply(2 * t * (1 - t))
        c = self.c.multiply(pow(t, 2))
        return Vector.sum([a, b, c])

    def _get_point_cubic(self, t) -> Vector:
        a = self.a.multiply(pow((1 - t), 3))
        b = self.b.multiply(3 * t * pow((1 - t), 2))
        c = self.c.multiply(3 * pow(t, 2) * (1 - t))
        d = self.d.multiply(pow(t, 3))
        return Vector.sum([a, b, c, d])


if __name__ == "__main__":
    bezier_points = [
        Bezier((0.3, 9), (0, 0), (0, 0), (2, 1)),
        # Bezier((0.3, 9), (0, 0), (2, 1)),
        # Bezier((0.3, 9), (2, 1)),
    ]

    dot = bezier_points[0].get_point(.55)
    print(dot)
    # for i in range(9):
    #     dot = bezier_points[0].get_point((i + 1) / 10.0)
    #     print("{0}\t{1}".format(dot[0], dot[1]))
