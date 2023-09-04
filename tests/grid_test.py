from mazes import Direction as D
from mazes import Grid


class TestGrid:
    def test_no_direction(self):
        d = D.Empty
        assert d == False

        assert d == 0

    def test_combo_directoins(self):
        d = D.Empty

        assert D.N not in d
        assert D.S not in d
        assert D.E not in d
        assert D.W not in d

        d = D.N | D.E

        assert D.N in d
        assert D.S not in d
        assert D.E in d
        assert D.W not in d

    def test_grid_creation(self):
        grid = Grid(2, 3)

        assert grid.width == 2
        assert grid.height == 3

        for y in range(0, 3):
            for x in range(0, 2):
                assert grid[x, y] == D.Empty, f"({x=}, {y=})"

    def test_index_out_of_bounds(self):
        grid = Grid(2, 3)

        assert grid[-1, 0] == None
        assert grid[1, -1] == None
        assert grid[2, 0] == None
        assert grid[0, 3] == None

    def test_setitem(self):
        grid = Grid(3, 3)

        grid[1, 1] = D.N | D.W

        assert grid[1, 1] == D.N | D.W

    def test_mark(self):
        grid = Grid(3, 3)

        grid.mark((1, 1), D.N)
        grid.mark((1, 1), D.W)

        assert grid[1, 1] == D.N | D.W

    def test_link(self):
        grid = Grid(3, 3)

        grid.link((1, 1), D.N)

        assert grid[1, 1] == D.N
        assert grid[1, 0] == D.S

    def test_link_multiple_individually(self):
        grid = Grid(3, 3)

        grid.link((1, 1), D.N)
        grid.link((1, 1), D.E)

        assert grid[1, 1] == D.N | D.E
        assert grid[1, 0] == D.S
        assert grid[2, 1] == D.W

    def test_link_multiple_at_once(self):
        grid = Grid(3, 3)

        grid.link((1, 1), D.N | D.E)

        assert grid[1, 1] == D.N | D.E
        assert grid[1, 0] == D.S
        assert grid[2, 1] == D.W

    def test_link_short_path(self):
        grid = Grid(3, 3)
        coord = grid.link_path((0, 0), [D.E, D.S])

        assert coord == (1, 1)
        assert grid[0, 0] == D.E
        assert grid[1, 0] == D.W | D.S
        assert grid[1, 1] == D.N

    def test_link_long_path(self):
        grid = Grid(3, 3)
        coord = grid.link_path((0, 0), [D.E, D.S, D.S, D.W, D.N, D.N])

        #     0   1   2
        #   +---+---+---+
        # 0 |       |   |
        #   +   +   +---+
        # 1 |   |   |   |
        #   +   +   +---+
        # 2 |       |   |
        #   +---+---+---+

        assert coord == (0, 0)

        assert grid[0, 0] == D.E | D.S
        assert grid[1, 0] == D.W | D.S

        assert grid[0, 1] == D.N | D.S
        assert grid[1, 1] == D.N | D.S

        assert grid[0, 2] == D.N | D.E
        assert grid[1, 2] == D.N | D.W

    def test_link_edge(self):
        grid = Grid(3, 3)

        grid.link((0, 0), D.W)
        grid.link((1, 0), D.N)

        assert grid[0, 0] == D.Empty
        assert grid[1, 0] == D.Empty

    def test_corners(self):
        grid = Grid(4, 3)

        assert grid.northwest_corner == (0, 0)
        assert grid.northeast_corner == (3, 0)
        assert grid.southwest_corner == (0, 2)
        assert grid.southeast_corner == (3, 2)

    def test_center(self):
        grid_3x3 = Grid(3, 3)
        grid_4x4 = Grid(4, 4)

        assert grid_3x3.center == (1, 1)
        assert grid_4x4.center == (2, 2)

    def test_has_direction(self):
        grid = Grid(3, 3)

        assert grid.valid_directions(grid.northwest_corner) == D.E | D.S
        assert grid.valid_directions(grid.northeast_corner) == D.W | D.S
        assert grid.valid_directions(grid.southwest_corner) == D.E | D.N
        assert grid.valid_directions(grid.southeast_corner) == D.W | D.N
        assert grid.valid_directions(grid.center) == D.N | D.S | D.E | D.W
