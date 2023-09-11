from .utils import remap

Color = tuple[int, int, int]


class ColorGradient:
    def __init__(self, start: Color, end: Color, steps: int) -> None:
        """
        A color gradient from `start` color to `end` color by using a table of
        size `steps`.
        """
        self._start = start
        self._end = end
        self._steps = steps

        r1, g1, b1 = self._start
        r2, g2, b2 = self._end

        table: list[Color] = []
        for i in range(steps):
            r = remap(0, steps - 1, r1, r2, i)
            g = remap(0, steps - 1, g1, g2, i)
            b = remap(0, steps - 1, b1, b2, i)
            color = (r, g, b)
            table.append(color)
        self._table = table

    def interpolate_float(self, val: float) -> Color:
        r1, g1, b1 = self._start
        r2, g2, b2 = self._end
        r = round((r1 - r2) * val) + r2
        g = round((g1 - g2) * val) + g2
        b = round((b1 - b2) * val) + b2
        return (r, g, b)

    def interpolate(self, val: int) -> Color:
        """
        Returns an interpolated color. `val` must be between `0` and `steps - 1`.
        """
        return self._table[val]
