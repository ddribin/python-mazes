import textwrap

def assert_render(actual: str, expected: str) -> None:
    __tracebackhide__ = True
    expected = textwrap.dedent(expected).lstrip()
    assert actual == expected
