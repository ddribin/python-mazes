from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


def my_range(start, stop, step=1) -> Iterator[int]:
    if stop <= start:
        raise RuntimeError(f"start ({start}) must be smaller than stop ({stop})")
    i = start
    while i < stop:
        yield i
        i += step


@dataclass
class RangerIncrementEvent:
    increment_by: int

    def opposite(self) -> RangerEvent:
        return RangerDecrementEvent(self.increment_by)


@dataclass
class RangerDecrementEvent:
    decrement_by: int

    def opposite(self) -> RangerEvent:
        return RangerIncrementEvent(self.decrement_by)


RangerEvent = RangerIncrementEvent | RangerDecrementEvent


def opposite_event(event: RangerEvent) -> RangerEvent:
    match event:
        case RangerIncrementEvent(i):
            return RangerDecrementEvent(i)
        case RangerDecrementEvent(i):
            return RangerIncrementEvent(i)


def next_event(iterator: Iterator[RangerEvent]) -> RangerEvent | None:
    try:
        event = next(iterator)
        return event
    except StopIteration:
        return None


class Ranger:
    @dataclass
    class IncrementEvent:
        n: int

        def opposite(self) -> Ranger.Event:
            return Ranger.DecrementEvent(self.n)

    @dataclass
    class DecrementEvent:
        n: int

        def opposite(self) -> Ranger.Event:
            return Ranger.IncrementEvent(self.n)

    Event = IncrementEvent | DecrementEvent

    @classmethod
    def next_event(cls, iterator: Iterator[Ranger.Event]) -> Ranger.Event | None:
        try:
            event = next(iterator)
            return event
        except StopIteration:
            return None

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if stop <= start:
            raise RuntimeError(f"start ({start}) must be smaller than stop ({stop})")
        self._start = start
        self._stop = stop
        self._step = step
        self._i = start

    @property
    def current(self) -> int:
        return self._i

    def my_range(self) -> Iterator[int]:
        while self._i < self._stop:
            yield self._i
            self._i += self._step

    def events(self) -> Iterator[Ranger.Event]:
        while self._i < self._stop:
            yield Ranger.IncrementEvent(self._step)

    def apply_event(self, event: Ranger.Event) -> None:
        match event:
            case Ranger.IncrementEvent(i):
                self._i += i
            case Ranger.DecrementEvent(i):
                self._i -= i


class TestGenerator:
    def test_generator_func(self) -> None:
        actual: list[int] = []
        for i in my_range(10, 15):
            actual.append(i)

        assert actual == [10, 11, 12, 13, 14]

    def test_generator_method(self) -> None:
        ranger = Ranger(10, 15)

        actual: list[int] = []
        for i in ranger.my_range():
            actual.append(i)

        assert actual == [10, 11, 12, 13, 14]

        actual = []
        for i in ranger.my_range():
            actual.append(i)

        assert actual == []

    def test_events(self) -> None:
        ranger = Ranger(10, 15)

        actual: list[int] = []
        events: list[Ranger.Event] = []
        for event in ranger.events():
            events.append(event)
            actual.append(ranger.current)
            ranger.apply_event(event)

        assert actual == [10, 11, 12, 13, 14]

    def test_event_iter(self) -> None:
        ranger = Ranger(10, 15)

        assert ranger.current == 10
        iter = ranger.events()

        for _ in range(10):
            event = Ranger.next_event(iter)
            assert event == Ranger.IncrementEvent(1)

        assert ranger.current == 10
        event = Ranger.next_event(iter)
        assert event is not None
        ranger.apply_event(event)
        assert ranger.current == 11
        # ranger.apply_event(opposite_event(event))
        # assert ranger.current == 10
        ranger.apply_event(event)
        assert ranger.current == 12
        ranger.apply_event(event.opposite())
        assert ranger.current == 11
        ranger.apply_event(event.opposite().opposite())
        assert ranger.current == 12
