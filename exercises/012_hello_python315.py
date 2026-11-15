"""Illustrate multiple Python 3.15 features."""

import re
import sys
import unicodedata
from collections import Counter
from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import datetime
from math import fmax, fmin, nan, signbit
from math.integer import isqrt
from pprint import pprint
from typing import Annotated, TypedDict, TypeForm
from zoneinfo import ZoneInfo
lazy import json
lazy import typing

type Pair = tuple[int, int]  # used in part_4_typeform


def part_1_lazy_imports() -> None:
    """Lazy imports."""
    # 1. Lazy imports
    print(f"before: {"json" in sys.modules=}")
    json_str = json.dumps({"title": "Postcards from the Edge", "year": 1990})
    print(f"{json_str=}")
    print(f"after: {"json" in sys.modules=}")
    print("=" * 50)


def part_2_starred_form_in_comprehensions() -> None:
    """Using */** in comprehensions."""
    # 2. Unpacking in comprehensions
    daily_temps = [[18.2, 21.7], [17.9], [19.4, 23.1]]
    config_items = [{"host": "db.local"}, {"port": 5432}]
    expected_temps = [18.2, 21.7, 17.9, 19.4, 23.1]
    expected_configs = {"host": "db.local", "port": 5432}

    ## old school flattening: nested loops
    temps = []
    for i in daily_temps:
        for j in i:
            temps.append(j)  # noqa: PERF402
    print(f"flattened: {temps}")
    assert temps == expected_temps

    configs = {}
    for i in config_items:
        for j in i:
            configs[j] = i[j]
    print(f"{configs=}")
    assert configs == expected_configs
    print("-" * 35)

    ## old school flattening: comprehensions
    temps = [j for i in daily_temps for j in i]
    print(f"flattened: {temps}")
    assert temps == expected_temps

    configs = {j: i[j] for i in config_items for j in i}
    print(f"{configs=}")
    assert configs == expected_configs
    print("-" * 35)

    ## using starred operator
    # pyrefly: ignore[not-a-type]
    temps = [*temps for temps in daily_temps]
    print(f"flattened: {temps}")
    assert temps == expected_temps

    configs = {**kv for kv in config_items}
    print(f"{configs=}")
    assert configs == expected_configs
    print("-" * 35)

    ## the starred form is supported in generator expressions too
    # pyrefly: ignore[bad-specialization, not-a-type]
    max_temp = max([*temps for temps in daily_temps])
    print(f"{max_temp}")
    # pyrefly: ignore[internal-error]
    assert max_temp == 23.1  # noqa: PLR2004
    # pyrefly: ignore[bad-specialization, no-matching-overload, not-a-type]
    sum_temps = sum([*temps for temps in daily_temps])
    print(f"{sum_temps}")
    assert sum_temps == 100.3  # noqa: PLR2004
    print("-" * 35)

    ## another example with dicts
    layers = [
        {"host": "localhost", "port": 8080},
        {"port": 5432},
        {"debug": True},
    ]
    expected = {"host": "localhost", "port": 5432, "debug": True}

    configs = {**items for items in layers}
    print(f"{configs=}")
    assert configs == expected
    print("=" * 50)


def part_3_new_builtin_types() -> None:
    """Illustrates the use of frozendict and sentinels."""
    # frozendict
    movie = {
        "title": "Late Night with the Devil",
        "year": 2023,
    }

    movie["rating"] = 7
    # pyrefly: ignore[bad-argument-count]
    frozen_movie = frozendict(movie)
    try:
        # pyrefly: ignore[unsupported-operation]
        frozen_movie["year"] = 2026
    except TypeError as e:
        print(f"error found: {e}")

    try:
        # pyrefly: ignore[unsupported-operation]
        frozen_movie["director"] = "Colin Cairnes"
    except TypeError as e:
        print(f"error found: {e}")
    print("-" * 35)

    # sentinel type
    MISSING = sentinel("MISSING")  # noqa: N806

    def get_option(
        options: dict[str, str | None],
        name: str,
        default: str | MISSING | None = MISSING,
    ) -> str | None:
        option = options.get(name, default)
        if option is MISSING:
            msg = "No default given and option was not found"
            raise KeyError(msg)
        return option

    result = get_option({"retries": None}, "retries")
    assert result is None

    result = get_option({}, "timeout", default=None)
    assert result is None

    try:
        result = get_option({}, "timeout")
    except KeyError as e:
        print(f"Expected: {type(e)} found")
    else:
        print("Expected exception not found!")

    result = get_option({"num_retries": None}, "num_retries")
    assert result is None

    result = get_option({"port": "8080"}, "num_retries", None)
    assert result is None

    result = get_option({"port": "8080"}, "num_retries", "3")
    assert result == "3"
    try:
        get_option({"port": "8080"}, "num_retries")  # KeyError!
    except KeyError as e:
        print(f"Expected: {type(e)} found")
    else:
        print("Expected exception not found!")
    print("=" * 50)


def part_4_typeform() -> None:
    """Illustrate how to use TypeForm to annotate functions."""

    # pyrefly: ignore[bad-return]
    def parse_old[T](value: str, typ: type[T]) -> T:
        """Empty implementation for illustration purposes."""

    # pyrefly: ignore[bad-return]
    def parse_new[T](value: str, typ: TypeForm[T]) -> T:
        """Empty implementation for illustration purposes."""

    # 1. Plain classes: both versions work the same way.
    typing.reveal_type(parse_old("42", int))  # int
    typing.reveal_type(parse_new("42", int))  # int
    typing.reveal_type(parse_old("42", list[int]))  # list[int]
    typing.reveal_type(parse_new("42", list[int]))  # list[int]

    # 2. Type expressions that are not classes: `type[T]` rejects them and
    #    can't solve T (revealed as `@_`), while `TypeForm[T]` accepts them
    #    and infers T from the expression.
    # pyrefly: ignore[bad-argument-type]
    typing.reveal_type(parse_old("42", None))  # @_
    typing.reveal_type(parse_new("42", None))  # None

    # pyrefly: ignore[bad-argument-type]
    typing.reveal_type(parse_old("42", Annotated[int, "meta"]))  # @_
    typing.reveal_type(parse_new("42", Annotated[int, "meta"]))  # int

    # pyrefly: ignore[bad-argument-type]
    typing.reveal_type(parse_old("42", Callable[[int], str]))  # @_
    typing.reveal_type(parse_new("42", Callable[[int], str]))  # (int) -> str

    # pyrefly: ignore[bad-argument-type]
    typing.reveal_type(parse_old("42", Pair))  # @_
    typing.reveal_type(parse_new("42", Pair))  # tuple[int, int]

    # pyrefly: ignore[bad-argument-type]
    typing.reveal_type(parse_old("42", "int"))  # @_
    typing.reveal_type(parse_new("42", "int"))  # int

    # 3. TypeForm still rejects values that are not type expressions.
    # pyrefly: ignore[bad-argument-type]
    typing.reveal_type(parse_new("42", 42))  # @_

    # 4. TypeForm can also annotate variables, and it is type checked.
    optional_int: TypeForm[int | None] = int | None
    typing.reveal_type(optional_int)  # TypeForm[int | None]
    # pyrefly: ignore[bad-assignment]
    wrong: TypeForm[int] = str  # type[str] isn't assignable to TypeForm[int]
    typing.reveal_type(wrong)  # TypeForm[int]
    print("=" * 50)


def part_5_typedict_closed_extra_items() -> None:
    """Illustrates the new parameters closed and extra_items."""

    class Movie(TypedDict, closed=True):
        title: str
        year: int

    movie = Movie(title="Postcards from the Edge", year=1990)
    print(movie)

    # It's only a pyrefly error, Python reports no error
    # pyrefly: ignore[bad-typed-dict-key]
    movie["rating"] = 6
    print(movie)

    class Headers(TypedDict, extra_items=str):
        content_type: str

    headers = Headers(content_type="text/plain")
    headers["x-trace-id"] = "12345"

    # Same thing here: only pyrefly gets it
    # pyrefly: ignore[bad-assignment]
    headers["content_length"] = 25

    print(headers)
    print("-" * 35)

    print(f"{Movie.__closed__=}")
    print(f"{Headers.__extra_items__=}")

    print("=" * 50)


def part_6_math_thingies() -> None:
    """Illustrates a few math related additions."""
    result = isqrt(2_000_000)
    print(f"{result=}")
    print("-" * 35)

    print(f"{max(1, nan)=}")
    print(f"{fmax(1, nan)=}")
    print(f"{max(nan, 1)=}")
    print(f"{fmax(nan, 1)=}")
    print("-" * 35)

    print(f"{min(1, nan)=}")
    print(f"{fmin(1, nan)=}")
    print(f"{min(nan, 1)=}")
    print(f"{fmin(nan, 1)=}")
    print("-" * 35)

    print(f"{signbit(0.0)}")
    print(f"{signbit(-0.0)}")

    print("=" * 50)


def part_7_re_prefix_match() -> None:
    """Introduces re.prefix_match() to match from the beginning of a str."""
    match = re.prefixmatch(r"\d{4}", "2026-11-14")
    if match:
        print(f"{match.group()=}")
    print("=" * 50)


def part_8_json_array_hooks() -> None:
    """Introduces the array_hook parameter in json.loads()."""
    result = json.loads("[1, 2, 3]")
    print(f"{result=}; ({type(result)})")
    result = json.loads("[1, 2, 3]", array_hook=tuple)
    print(f"{result=}; ({type(result)})")
    print("=" * 50)


def part_9_pprint_expand() -> None:
    """Illustrates the new parameter expand in pprint."""
    config = {
        "name": "backup",
        "targets": ["/home", "/etc"],
        "schedule": {"hour": 3, "days": ["mon", "thu"]},
    }
    pprint(config)
    pprint(config, expand=True)
    print("=" * 50)


def part_10_iter_graphemes() -> None:
    """Illustrates the use of unicodedata.iter_graphemes()."""
    for i, g in enumerate(unicodedata.iter_graphemes("Hello 🇪🇸!")):
        print(f"{i}: {g}")
    print("-" * 35)

    for i, c in enumerate("Hello 🇪🇸!"):
        print(f"{i}: {c}")
    print("=" * 50)


def part_11_bytearray_take_bytes() -> None:
    """Using bytearray.take_bytes to read bytes from the front of a buffer."""
    buffer = bytearray(b"HTTP/1.1 200 OK\r\nRest of the request")
    protocol = buffer.take_bytes(8)
    print(f"{protocol=}; rem_buffer={buffer}")
    print("=" * 50)


def part_12_counter_caret_operator() -> None:
    """Using the ^ for computing the symmetric difference with counters."""
    counter1 = Counter(nostra=3, frutti_di_mare=1)
    counter2 = Counter(nostra=1, frutti_di_mare=1, ragazzi=2)

    print(f"{counter1 ^ counter2=}")
    print("=" * 50)


def part_13_iso_date_shorthand() -> None:
    """Illustrates how to use %F to parse dates in ISO format."""
    today = "2026-11-15"
    today_as_date = datetime.strptime(today, "%F").replace(
        tzinfo=ZoneInfo("Europe/Madrid"),
    )
    print(f"{today_as_date=}")
    print("=" * 50)


def part_14_pattern_matching_positive_sign() -> None:
    """Using how to use positive sign cases in structural pattern matching."""

    def classify(delta: int) -> str:
        """Return a direction depending on the delta received."""
        match delta:
            case -1:
                return "down"
            case +1:
                return "up"
            case 0:
                return "flat"
            case _:
                msg = f"Only -1, 0, 1 are accepted but got {delta}"
                raise ValueError(msg)

    print(f"{classify(0)}")
    print(f"{classify(1)}")
    print(f"{classify(+1)}")
    print(f"{classify(-1)}")
    print("=" * 50)


def part_15_ctx_manager_in_generators() -> None:
    """Illustrates the behavior of @contextmanager with generators."""

    @contextmanager
    def logged(label: str) -> Generator[None]:
        print(f">> enter {label}")
        yield
        print(f">> exit {label}")

    @logged("read_lines")
    def read_lines() -> Generator[str]:
        yield "first"
        yield "second"

    for line in read_lines():
        print(f"{line=}")
    print("=" * 50)


def main() -> None:
    """Application entry point."""
    part_1_lazy_imports()
    print()

    part_2_starred_form_in_comprehensions()
    print()

    part_3_new_builtin_types()
    print()

    part_4_typeform()
    print()

    part_5_typedict_closed_extra_items()
    print()

    part_6_math_thingies()
    print()

    part_7_re_prefix_match()
    print()

    part_8_json_array_hooks()
    print()

    part_9_pprint_expand()
    print()

    part_10_iter_graphemes()
    print()

    part_11_bytearray_take_bytes()
    print()

    part_12_counter_caret_operator()
    print()

    part_13_iso_date_shorthand()
    print()

    part_14_pattern_matching_positive_sign()
    print()

    part_15_ctx_manager_in_generators()
    print()


if __name__ == "__main__":
    main()
