from mazes import Grid, Direction as D

def test_opposite_directions():
    assert D.N.opposite() == D.S
    assert D.S.opposite() == D.N
    assert D.E.opposite() == D.W
    assert D.W.opposite() == D.E

class TestGrid:
    def test_opposite_directions(self):
        assert D.N.opposite() == D.S
        assert D.S.opposite() == D.N
        assert D.E.opposite() == D.W
        assert D.W.opposite() == D.E

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

