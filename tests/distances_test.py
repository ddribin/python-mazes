from mazes import Distances


class TestDistances:
    def test_initial_state(self):
        distances = Distances(3, 4, (0, 0))

        assert distances.width == 3
        assert distances.height == 4
        assert distances.root == (0, 0)
        assert distances.max_coordinate == (0, 0)
        assert distances.max_distance == 0

        for y in range(4):
            for x in range(3):
                assert distances[x, y] == None

    def test_setting_distances(self):
        distances = Distances(3, 3, (0, 0))
        distances[0, 1] = 1
        distances[1, 1] = 2

        assert distances.max_coordinate == (1, 1)
        assert distances.max_distance == 2

        for y in range(3):
            for x in range(3):
                if x == 0 and y == 1:
                    assert distances[x, y] == 1
                elif x == 1 and y == 1:
                    assert distances[x, y] == 2
                else:
                    assert distances[x, y] == None
