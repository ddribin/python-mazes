from mazes import Grid, Direction as D

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

    def test_link_multiple(self):
        grid = Grid(3, 3)

        grid.link((1, 1), D.N)
        grid.link((1, 1), D.E)

        assert grid[1, 1] == D.N | D.E
        assert grid[1, 0] == D.S
        assert grid[2, 1] == D.W
    

    def test_link_edge(self):
        grid = Grid(3, 3)

        grid.link((0, 0), D.W)
        grid.link((1, 0), D.N)

        assert grid[0, 0] == D.Empty
        assert grid[1, 0] == D.Empty
