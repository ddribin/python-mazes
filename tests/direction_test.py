from mazes import Grid, Direction as D

class TestDirection:
    def test_opposite_directions(self):
        assert D.N.opposite() == D.S
        assert D.S.opposite() == D.N
        assert D.E.opposite() == D.W
        assert D.W.opposite() == D.E
