def remap(a: int, b: int, c: int, d: int, x: int) -> int:
    """
    Remaps x in the range [a;b] to the range [c;d] (inclusive).
    Taken from: https://blog.pkh.me/p/29-the-most-useful-math-formulas.html
    """
    n = x * (d - c) // (b - a) + c - a * (d - c) // (b - a)
    return n


def remap_zero(b: int, d: int, x: int) -> int:
    """
    Remaps x in the range [0;b] to the range [0;d] (inclusive).
    Taken from: https://blog.pkh.me/p/29-the-most-useful-math-formulas.html
    """
    n = (x * d) // b
    return n
