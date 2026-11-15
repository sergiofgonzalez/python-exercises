"""Simple function definition and invocation."""


def square(x: float) -> float:
    """Compute the square of the given number.

    Args:
        x: The number to square.

    Returns:
        The square of ``x``.
    """
    return x * x


def main() -> None:
    """Application entry point."""
    x = 3
    print(f"{square(x)=}")

    y = 1.23
    print(f"{square(y)=}")

    result = square(5)
    print(f"{result=}")


if __name__ == "__main__":
    main()
