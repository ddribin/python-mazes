import textwrap

from mazes.distances import ImmutableDistances


def assert_render(actual: str, expected: str) -> None:
    #    __tracebackhide__ = True
    expected = textwrap.dedent(expected).lstrip()
    assert actual == expected


def assert_distances(distances: ImmutableDistances, expected: list[list[int]]) -> None:
    for y in range(distances.height):
        for x in range(distances.width):
            assert distances[x, y] == expected[y][x], f"({x=}, {y=})"
