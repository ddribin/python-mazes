from mazes import Direction as D


class TestDirection:
    def test_opposite_directions(self):
        assert D.N.opposite() == D.S
        assert D.S.opposite() == D.N
        assert D.E.opposite() == D.W
        assert D.W.opposite() == D.E

    def test_update_coordinate(self):
        assert D.N.update_coordinate((2, 2)) == (2, 1)
        assert D.S.update_coordinate((2, 2)) == (2, 3)
        assert D.E.update_coordinate((2, 2)) == (3, 2)
        assert D.W.update_coordinate((2, 2)) == (1, 2)

        dir = D.N | D.W
        assert dir.update_coordinate((2, 2)) == (1, 1)

    def test_invert(self):
        assert D.Empty.invert == (D.N | D.S | D.E | D.W)
        assert (D.N | D.S | D.E | D.W).invert == D.Empty
        assert D.N.invert == (D.S | D.E | D.W)
        assert (D.S | D.E | D.W).invert == D.N
