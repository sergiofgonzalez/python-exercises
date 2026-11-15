# Exercises from Python workbench

## 010: Hello, Python

Create a hello, world Python project to make sure that you have your environment correctly created by creating a hello world program using `uv`. Configure the project to use the latest stable Python version (e.g., 3.13.3 at the time of writing).

### Solution

Create a minimal project (plain `uv init` scaffolds more than needed):

```zsh
uv init --bare exercises
```

This creates only `pyproject.toml`. Then add `010_hello_python.py`.

#### Tooling

- **Ruff** (lint + format): `uv add --dev ruff`. Install the Ruff VS Code extension, set it as the default formatter, and enable format on save. `pyproject.toml` uses `select = ["ALL"]` with the Google docstring convention.
- **Pyrefly** (type checking): `uv add --dev pyrefly` and its VS Code extension. `uv run pyrefly init` adds a `[tool.pyrefly]` section to `pyproject.toml`.
- **Even Better TOML**: VS Code extension for editing `pyproject.toml`.

## 011: Hello, Pyrefly

Pyrefly is Meta's new static type checker, used for all the exercises. Install it with:

```zsh
uv add --dev pyrefly
```

1. Write a function `average()` that takes a list of ints or floats and returns their average. It must raise a `ValueError` if the list is empty.
2. Annotate it with type hints and call it with `["a", "b", "c"]`. Run the program, then run `uv run pyrefly check 011_hello_pyrefly.py`. What's the difference?
3. Write a function `maximum()` that returns the largest of the given numbers, without type hints. Call it with a list of numbers and run `uv run pyrefly infer 011_hello_pyrefly.py`. What happens if you run it without calling the function first?
4. Write a function `minimum()` and annotate it by hand using `Collection` instead of `list`.
5. Call the three functions with a set or tuple instead of a list, run `pyrefly check`, and report the results.
6. Write a function `count()` that return the number of values passed that are not zero or `None`. For example, `count([1, 0, `None`, 4]) = 4`. Do not add type hints to the function.
7. Explore `uv run pyrefly coverage check <file> --fail-under <min_coverage> --strict`. `--fail-under` lets you adjust the min coverage and `strict` considers types annotated as `Any` as if they were untyped. Play with the types of `count()` to see how the parameters work.
8. Explore `uv run pyrefly coverage report` to see a report of the type coverage within your file.

### Solution

VS Code setup:

- **Python › Analysis: Diagnostics Source** set to "Pylance + Pyrefly", so Pyrefly reports the diagnostics.
- **Python › Analysis: Pyrefly Version** left empty to use the latest release.

Results:

- **`average()`**, annotated with `list[int | float]`: calling it with strings raises a `TypeError` only at runtime, whereas `pyrefly check` reports the error before the code runs.
- **`maximum()`**: `pyrefly infer` adds nothing until the function is called, because it infers parameter types from call sites. After adding a call, the first run annotated the parameter as `list[int | float]` and a second run added the return type, which can only be inferred once the parameter type is known.
- **`minimum()`**, annotated with `Collection[int | float]`: with tuples and sets, it's the only call Pyrefly doesn't flag. Inferred types only reflect how a function was called, while a hand-written annotation can describe everything it accepts.
- **`count()`** and `pyrefly coverage check`: coverage is measured over *typable* slots, meaning each parameter and each return type. The file has 9: two per function, and one for `main()`, which has no parameters.
  - **No type hints:** 7 of 9 typed (77.78%). The check fails by default, since `--fail-under` defaults to 100%, and it also fails with `--fail-under 80`. With `--fail-under 75` it passes, but still warns that `count` is not fully typed.
  - **`numbers: Any`:** `Any` counts as typed, so coverage rises to 8 of 9 (88.89%) and `--fail-under 80` passes. The missing return type still triggers a `coverage-partial` warning.
  - **`--strict`:** `Any` counts as untyped, so coverage drops back to 7 of 9 (77.78%) and `--fail-under 80` fails again. `count` is now reported as `coverage-missing`.
- **`pyrefly coverage report`:** outputs a JSON report with a `symbol_reports` entry for each function, giving its `n_typable`, `n_typed`, `n_any` and `n_untyped` counts. For `count()` with `Any`, this shows `n_typed: 0, n_any: 1, n_untyped: 1`. The report keeps `Any` separate from real types, and it's what `--strict` uses to decide whether `Any` counts as typed.

## 012: Hello, Python 3.15 features!

This repo uses Python 3.15. It was created using `uv init --python 3.15`.

### Lazy import statements

The `lazy` keyword lets you keep your imports at the top of your Python file, but defers the work of importing it until you first use the module.

Create a program that import `sys` in the standard mode but lazy imports the `json` module.

Then, write a line inspects `sys.modules` first printing whether the `"json"` module is in there.

Then, use `json.dumps()` to create a JSON of a dictionary of your choice. Then, inspect again `sys.modules` to see if `"json"` module has been loaded.

### Solution

To check if a module has been loaded you need to use its name as a string:

```python
"json" in sys.modules
```

Also, remember that `json.dumps()` takes a Python object and serializes it as a JSON string.

### Unpacking in comprehensions

Python 3.15 allows you to use `*` and `**` directly inside comprehensions, which become very useful when flattening list of lists, or lists of dicts.

Given the list of daily temperatures: `[[18.2, 21.7], [17.9], [19.4, 23.1]]` and a list of config items: `[{"host": "db.local"}, {"port": 5432}]`:

1. Write some code that flattens those lists so that the result is: `[18.2, 21.7, 17.9, 19.4, 23.1]` and `{'host': 'db.local', 'port': 5432}`.

2. Repeat the exercises using `*` and `**` within the comprehensions to obtain the same results.

3. To illustrate that generator expressions support the starred form too, invoke `max()` and `sum()` with the list of daily temperatures without using an intermediary list. It should render 23.1 and 100.3 respectively

4. To illustrate how to use it with dict comprehensions, consider the following dict:

    ```python
    layers = [
        {"host": "localhost", "port": 8000},
        {"port": 5432},
        {"debug": True},
    ]
    ```

    Write a snippet that transforms `layers` into: `{'host': 'localhost', 'port': 5432, 'debug': True}`

    Note that later key wins.

### New built-in types

`frozendict` has been introduced to freeze dictionaries (similar to what tuples do to lists, or frozensets do to sets).

1. Create a frozen dictionary of your choice (use `frozendict(dict)`). Try to edit one of the key values, or add a key an see what happens.


`sentinel` is a new type for missing values. It is typically helpful when `None` is a meaningful value in the given context.

1. Define a `sentinel` value `MISSING` (use `sentinel("MISSING")`).
2. Define a function `get_option(options, name, default=MISSING)` which gets the value associated to the given name or the default. If the default was not given and the value for the key wasn't found, a `KeyError` should be raised. Otherwise, the value should be returned.

For example, invoking the function with:

```python
get_option({"retries": None}, "retries") # -> None
get_option({}, "timeout", default=None)  # -> None
get_option({}, "timeout")                # -> KeyError
```

#### Solution

The `frozendict` part is trivial, but the sentinel values require a little elaboration.

The function implementation is as follows:

```python
MISSING = sentinel("MISSING")  # noqa: N806

def get_option(options, name, default=MISSING):
    option = options.get(name, default)
    if option is MISSING:
        msg = "No default given and option was not found"
        raise KeyError(msg)
    return option
```

We use `options.get()` as we would do in older versions of Python, but then, instead of checking if option is `None`, we check against `MISSING`. That let us distinguish between `None` (a potential valid value sent by the client) and the situation in which the client code didn't send any value:

```python
# option available, no default value provided
get_option({"num_retries": None}, "num_retries") # -> None 

# option not found, default value of None provided
get_option({"port": "8080"}, "num_retries", None) # -> None

# option not found, default value != None provided
get_option({"port": "8080"}, "num_retries", 3) # -> 3

# option not found, default value not provided
get_option({"port": "8080"}, "num_retries") # KeyError!
```


### Anotating type forms with `TypeForm`

Some functions take a type as an argument and return a value of that type.

Until now, such functions were annotated with `type[T]`. That only accepts actual classes, such as `int` or `list[int]`. Many valid *type expressions* are not classes, for example `None`, `Annotated[int, ...]`, `Callable[[int], str]`, a `type` alias, or a forward reference string like `"int"`. With `type[T]`, the type checker rejects them and can't work out what `T` is.

`TypeForm[T]` (PEP 747) accepts any valid type expression and infers `T` from it. It still rejects values that aren't type expressions, such as `42`.

Create a couple of functions:
- `parse_old[T](value: str, typ: type[T]) -> T`
- `parse_new[T](value: str, typ: TypeForm[T]) -> T`

Then wrap calls to both in `typing.reveal_type`, run `pyrefly check`, and compare the results. Pyrefly 1.4.1 reports:

| Argument | `parse_old` (`type[T]`) | `parse_new` (`TypeForm[T]`) |
|---|---|---|
| `int` | `int` | `int` |
| `list[int]` | `list[int]` | `list[int]` |
| `None` | error, `@_` | `None` |
| `Annotated[int, "meta"]` | error, `@_` | `int` |
| `Callable[[int], str]` | error, `@_` | `(int) -> str` |
| `Pair` (from `type Pair = tuple[int, int]`) | error, `@_` | `tuple[int, int]` |
| `"int"` | error, `@_` | `int` |
| `42` | error, `@_` | error, `@_` |

`@_` means Pyrefly couldn't solve `T`, so the caller gets no useful return type.

`TypeForm` can also annotate variables, and Pyrefly checks the assignment:

```python
optional_int: TypeForm[int | None] = int | None  # OK
wrong: TypeForm[int] = str  # error: type[str] is not assignable to TypeForm[int]
```

> **Note:** Pyrefly is lenient with `type[T]`. It accepts `int | None` and `Literal[...]` for it, even though stricter checkers such as mypy reject `int | None`. That's why those two aren't in the table.

### Closed `TypedDict` types and extra items

A `TypedDict` describes a dict with known keys, but until now it didn't say anything about keys it didn't list.

Now you can do the following:

```python
from typing import TypedDict

class Movie(TypedDict, closed=True):
    title: str
    year: int

class Headers(TypedDict, extra_items=str):
    content_type: str
```

Create such TypedDict's and then:
- instantiate a movie including the extra key "rating"
- headers including content-type but also a x-trace-id key with a string value
- another headers instance with content-type and x-retries key with an int value

Then print:
+ `Movie.__closed__`
+ `Headers.__extra_items`

Then run the program and pyrefly and report what you get.

#### Solution

The first thing to notice is that those parameters are for the type checkers and not for the runtime. When you run the program you get 0 errors.

If you run `uv run pyrefly check` you'll get notified of those errors.

### The Python sampling profiler

The standard library now ships Tachyon in the new profiling package. It's a statistical profiler that samples the stack from outside the process.

You can run it using:

```zsh
uv run --python 3.15 \
  python -m profiling.sampling \
  run <program>.py
```

The report you get after executing it will tell you where most of the time is lost.

Create a program that performs the following:

1. Invoke a `greet_me()` function.
2. Invokes a function that executes a loop over the first 1000 ints computing its sum
3. Invokes a function that flattens a 3x3 matrix using the starred unpacking.
4. Invokes a function that flattens the same 3x3 matrix using nested loops.
5. Invokes a function that prints a string with variable parts (received as parameters in the function) using `+`.
6. Invokes a function that prints a string with variable parts (received as parameters in the function) using an f-string.

#### Solution

Not implemented. The new profiler requires admin rights, which I don't have on my Mac.

### The new `math.integer` submodule

The `math` module has always focused on floating-point numbers, which made `math.factorial()` and other integer-related functions feel weird. Now it's easier to enforce integer arithmetics with that new `math.integer` submodule.

1. Import `math.integer`
2. Compute the integer square root of the number 2,000,000

### New floating-point helpers

The functions `fmax()` and `fmin()` now work properly with NaN, and `signbit()` distinguishes between `0.0` and `-0.0`.

Create a small snippet that compares the behaviors of `max` vs `fmax`, `min` vs. `fmin` (especially when passing NaN as first argument vs. passing it as a second argument) and the behavior of `signbit` when passed `0.0` and `-0.0`.

### Soft-deprecation of `re.match()`

The function `re.match()` matches at the start of the string, which is confusing. Now, a new function `re.prefixmatch()` is introduced instead to make it superclear where the matching starts. As a result, `re.match` is sort of soft-deprecated.

Use `re.prefixmatch()` to extract the year as a group from a date. Compare it with `re.match()` (should be the same).

### `array_hook` parameter in `json.loads()`

The new parameter `array_hook` lets you parse JSON arrays into something other than Python lists.

Test it by creating a snippet that loads the JSON array `[1, 2, 3]` and serializes it into a Python tuple. Compare it with the default behavior.

### `expand` parameter in `pprint`

The `pprint` module now accepts a new expand argument that when a container doesn't fit on one line, prints one item per line, a trailing comman, and the closing bracket on its own line.

Print the following object with `expand=True` and compare it with the default behavior:

```python
config = {
    "name": "backup",
    "targets": ["/home", "/etc"],
    "schedule": {"hour": 3, "days": ["mon", "thu"]},
}
```

### `unicodedata.iter_graphemes()` to split text

When splitting text containing emojis, etc. the usual functions to split into characters don't work well. The new function `unicodedata.iter_graphemes()` helps with that.

Split the text `"Hello 🇪🇸!"` by perceived characters.

## `bytearray.take_bytes()`

The new method `bytearray.take_bytes()` removes the number of given bytes from the front of the buffer and returns it without making a copy.

Familiarize yourself with it using the bytearray: `b"HTTP/1.1 200 OK\r\nRest of the request"`.

## The `^` operator `collections.Counter`

The `^` in `collections.Counter` returns the symmetric difference between two counters. That is:

Create a `Counter(nostra=3, frutti_di_mare=1)` and a `Counter(nostra=1, frutti_di_mare=1, ragazzi=2)` and compute the results of applying the symmetric difference to both.

Note that `frutti_di_mare` won't be reported in the results because its count is the same on both.

## ISO date shorthand

The `datetime.strptime()` method understands the `%F` directive for ISO dates to parse dates in format `2026-10-12`.

## Structural pattern matching now supports positive sign

Define a function `classify(delta)` which uses structural pattern matching to report:
- up when receives 1
- down when receives -1
- flat when returns 0

Within the function, use `+1`, `-1` and `0` in the cases of the pattern matching.

## New behavior for functions using `@contextmanager` in generators

In Python 3.14, using `@contextmanager` with generators was permitted but the context closed as soon as the generator object was created (even before the loop even started). Now it works correctly in Python 3.15.

1. Define a function `logged(label)` decorated with `@contextmanager` that prints:
    1. enter {label}
    2. yields
    3. exit {label}

2. Use that decorator on a function `read_lines()` that yields "first" and then yields "second`.

3. Use a for that iterates over the results of `read_lines` printing them.

Compare the behavior of both programs in Python 3.14 and 3.15.

HINT: use `uv run --python 3.14 python <program>.py`

## Looking to upgrade

If you're planning to upgrade and your project uses `uv` you can use the `--isolated` flag and `-W error::DeprecationWarning` to get a test errors instead of warnings.

That is, you can run:

```zsh
uv run --isoalated --python 3.15 \
  pytest -W error:DeprecationWarning
```


## 013: Understanding sentinel values in Python
> https://realpython.com/python315-sentinel-values/


## 014: Hello, t-strings
> https://realpython.com/python-t-strings/

## 021: Hello, function

Write a function that squares a number and print its result.

### Solution

The function was trivial, so I used the exercise to set up VSCode:

- Pyrefly as the only language server (Pylance disabled).
- Inlay hints for inferred types and argument names.
- Google-style docstrings.

### 022: Higher-order function

Create a function `add(x, y)` that sums up the numbers received as arguments, and a function `sub(x, y)` that subtracts those numbers.

Define the function `compute(x, y, op)` that receives as argument two numbers and a function such as `add()` and `sub()` and use it to perform some calculations.

#### Solution

Functions are first-class objects, so `add` and `sub` can be passed to `compute()` like any other value:

- `op` is annotated by hand as `Callable[[float, float], float]`.
- `Callable` is only needed for annotations, so it's imported with a `lazy` import (Python 3.15+).
- Added a VSCode ruler at column 79 to match Ruff's `line-length` setting.

### 023: Using functions from the `math` library

Write a program that imports the `math` library in your program to:

+ print the value of $ \pi $ and $ e $.
+ compute the square $ \sqrt{144} $.
+ compute $ sin(2 \cdot \pi) $

### 024: Using complex numbers

Python supports math operations with complex numbers. Define the complex numbers $ 3 + i $ and $ 100 + 10 i $, with $ i $ being the imaginary part.

Hint: use `j` to represent the imaginary part.

### 025: Generating random numbers

Using the `random` library from Python's standard libary:

+ produce a random integer between 0 and 10 (inclusive).
+ produce a random floating point number between 7.5 and 10.5 (HINT: use `uniform`)