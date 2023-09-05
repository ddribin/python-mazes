from itertools import chain
from typing import TypeVar

T = TypeVar("T")


def unwrap(x: T | None) -> T:
    assert x is not None
    return x


def flatten(lst: list[list[T]]) -> list[T]:
    return list(chain.from_iterable(lst))
