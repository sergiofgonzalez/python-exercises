"""Illustrate Pyrefly capabilities with several examples ."""

from typing import Any
lazy from collections.abc import Collection


def average(numbers: list[int | float]) -> int | float:
    """Computes the averages of the numbers given."""
    if not numbers:
        msg = "a list with at least one number is required"
        raise ValueError(msg)
    return sum(numbers) / len(numbers)


def maximum(numbers: list[int]) -> int:
    """Returns the maximum among the numbers given."""
    if not numbers:
        msg = "a list with at list one number is required"
        raise ValueError(msg)
    return max(numbers)


def minimum(numbers: Collection[int | float]) -> int | float:
    """Returns the minumum among the numbers given."""
    if not numbers:
        msg = "a list with at list one number is required"
        raise ValueError(msg)
    return min(numbers)


def count(numbers: Any):  # noqa: ANN201, ANN401
    """Return the count of values that are not zero or empty."""
    return sum(1 if num else 0 for num in numbers)


def main() -> None:
    """Application entry point."""
    result = average([1, 2, 3])
    print(f"{result=}")

    # Forcing an error:
    # TypeError: unsupported operand types for +
    # average(["a", "b", "c"])  # noqa: ERA001

    result = maximum([1, 2, 3])
    print(f"{result=}")

    # print(f"average((1, 2, 3))={average((1, 2, 3))}")  # noqa: ERA001
    # print(f"maximum({{1, 2, 3}})={maximum({1, 2, 3})}")  # noqa: ERA001
    print(f"minimum((1, 2, 3)={minimum((1, 2, 3))}")

    print(f"count([1, 0, None, 4])={count([1, 0, None, 4])}")


if __name__ == "__main__":
    main()
