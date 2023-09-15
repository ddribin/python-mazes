from mazes import AlgorithmType, MazeOptions


class TestMazeGenerator:
    def test_maze_options_default_values(self) -> None:
        options = MazeOptions(2, 3)

        assert options.width == 2
        assert options.height == 3
        assert options.algorithmType == AlgorithmType.RecursiveBacktracker
        assert options.start == (0, 0)
        assert options.end == (1, 2)
        assert options.seed is None
