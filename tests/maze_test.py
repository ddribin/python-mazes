from mazes import Maze

def test_maze():
    m = Maze()
    assert m.increment(3) == 4
