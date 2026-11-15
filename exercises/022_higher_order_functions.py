"""Demonstrate the use of higher-order functions."""

lazy from collections.abc import Callable


def add(x: float, y: float) -> float:
    """Compute the sum of the given numbers.

    Args:
        x: The first number to sum.
        y: The second number to sum.

    Returns:
        The sum of ``x`` and ``y``.
    """
    return x + y


def sub(x: float, y: float) -> float:
    """Compute the difference of the given numbers.

    Args:
        x: The number to subtract from.
        y: The number to subtract.

    Returns:
        The result of subtracting ``y`` from ``x``.
    """
    return x - y


def compute(x: float, y: float, op: Callable[[float, float], float]) -> float:
    """Return the result of applying an operation to the given numbers.

    Args:
        x: the first operand.
        y: the second operand.
        op: the operation to be applied

    Returns:
        The result of applying the operation to the given operands, that is
        ``op(x, y)``
    """
    return op(x, y)


def main() -> None:
    """Application entry point."""
    x = 1
    y = 2
    print(f"add({x}, {y})={add(x, y)}")

    print(f"sub({y}, {x})={sub(y, x)}")

    # higher-order function test
    print(f"op({x}, {y}, {add.__name__})={compute(x, y, add)}")
    print(f"op({y}, {x}, {sub.__name__})={compute(x, y, sub)}")


if __name__ == "__main__":
    main()
