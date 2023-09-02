import random
from typing import TypeVar, Sequence
from itertools import chain

T = TypeVar("T")


def sample(l: Sequence[T]) -> T:
    index = random.randint(0, len(l) - 1)
    return l[index]


def unwrap(x: T | None) -> T:
    assert x is not None
    return x


def flatten(l: list[list[T]]) -> list[T]:
    return list(chain.from_iterable(l))
