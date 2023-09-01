import random
from typing import TypeVar, Sequence

T = TypeVar("T")


def sample(l: Sequence[T]) -> T:
    index = random.randint(0, len(l) - 1)
    return l[index]


def unwrap(x: T | None) -> T:
    assert x is not None
    return x
