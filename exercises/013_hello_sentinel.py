"""Illustrate the basics of the sentinel type in Python 3.15."""

import pickle
from copy import deepcopy
from pathlib import Path
from typing import Any
lazy import tomllib
lazy from collections.abc import Generator

MISSING = sentinel("MISSING")
UNSET = sentinel("UNSET", repr="<unset>")
STOP = sentinel("STOP")
NO_DEFAULT = sentinel("NO_DEFAULT")
DONE = sentinel("DONE")


def part_1_hello_sentinel_basics() -> None:
    """Basics of sentinel."""
    # 1. Define and print a sentinel
    print(MISSING)
    print("-" * 35)

    # 2. Define asentinel with a custom repr and print it
    print(UNSET)
    print("-" * 35)

    # 3. Comparing sentinels
    try:
        assert STOP == MISSING
    except AssertionError as e:
        print(f"Can't compare sentinels with ==  {e}")

    assert STOP is not MISSING
    assert STOP is STOP  # noqa: PLR0124
    stop_var = STOP
    assert stop_var is STOP
    print("-" * 35)

    # 4. Sentinel type
    print(f"{type(MISSING)=}")
    print(f"{type(UNSET)=}")
    assert type(MISSING) is type(UNSET)
    assert isinstance(MISSING, sentinel)
    print("=" * 50)


def part_2_sentinel_for_missing_values() -> None:  # noqa: C901, PLR0915
    """Using sentinels for dealing with missing values."""

    # 5. Using sentinels for dealing with missing values
    def get_setting(
        config: dict[str, Any],
        path: str,
        *,
        default: str | int | NO_DEFAULT = NO_DEFAULT,
    ) -> str:
        """Read a dotted path config value.

        Reads a dotted path like "db.timeout" and returns the corresponding
        value from the config.
        When the path doesn't exist, callers can supply a default value.
        Callers that don't pass a default value for paths that don't exist will
        get a KeyError exception
        """
        path_components = path.split(".")
        i = 0
        while i < len(path_components) - 1 and path_components[i] in config:
            config = config[path_components[i]]
            i += 1
        value = config.get(path_components[-1], default)
        if value is NO_DEFAULT:
            msg = f"{path} not found"
            raise KeyError(msg)
        return value

    def get_setting_v2(
        config: dict[str, Any],
        path: str,
        *,
        default: int | str | NO_DEFAULT = NO_DEFAULT,
    ) -> Any:  # noqa: ANN401
        """Read a dotted path config value (cleaner implementation)."""
        for path_component in path.split("."):
            try:
                config = config[path_component]
            except KeyError:
                if default is NO_DEFAULT:
                    msg = f"{path} not found"
                    raise KeyError(msg) from None
                return default
        return config

    path_to_config = Path("./data/in/db_config.toml")
    with path_to_config.open("rb") as config_file:
        config = tomllib.load(config_file)
        assert get_setting(config, "db.timeout") == 30  # noqa: PLR2004
        assert get_setting(config, "db.port", default=5432) == 5432  # noqa: PLR2004

        try:
            get_setting(config, "db.port")
        except KeyError as e:
            print(f"Expected exception: {e} ({type(e)})")

        # Unhappy path: root not fnd, with child key, with and without default
        assert get_setting(config, path="web.num_retries", default=3)
        try:
            get_setting(config, path="web.num_retries")
        except KeyError as e:
            print(f"Expected exception: {e} ({type(e)})")

        # Unhappy path: root not found, no child key, with and without default
        assert get_setting(config, "NUM_RETRIES", default=3)
        try:
            get_setting(config, "NUM_RETRIES")
        except KeyError as e:
            print(f"Expected exception: {e} ({type(e)})")
        print("-" * 35)

        assert get_setting_v2(config, "db.timeout") == 30  # noqa: PLR2004
        assert get_setting_v2(config, "db.port", default=5432) == 5432  # noqa: PLR2004

        try:
            get_setting_v2(config, "db.port")
        except KeyError as e:
            print(f"Expected exception: {e} ({type(e)})")

        # Unhappy path: root not fnd, with child key, with and without default
        assert get_setting_v2(config, path="web.num_retries", default=3)
        try:
            get_setting_v2(config, path="web.num_retries")
        except KeyError as e:
            print(f"Expected exception: {e} ({type(e)})")

        # Unhappy path: root not found, no child key, with and without default
        assert get_setting_v2(config, "NUM_RETRIES", default=3)
        try:
            get_setting_v2(config, "NUM_RETRIES")
        except KeyError as e:
            print(f"Expected exception: {e} ({type(e)})")
        print("=" * 50)


def part_3_sentinel_safe_to_copy() -> None:
    """Demonstrate sentinels are safe in copy/deepcopy/pickle operations."""

    def parse_patch(
        form: dict[str, str | None],
    ) -> dict[str, str | MISSING | None]:
        """Return a patch dict from the form data received."""
        return {
            "name": form.get(
                "name",
                MISSING,
            ),  # form["name"] if "name" in form else MISSING,
            "bio": form.get("bio", MISSING),
            "email": form.get("email", MISSING),
        }

    def apply_patch(
        profile: dict[str, str | None],
        patch: dict[str, str | MISSING | None],
    ) -> dict[str, str | None]:
        """Return the updated profile after applying the patch."""
        return {
            "name": profile["name"]
            if patch["name"] is MISSING
            else patch["name"],
            "bio": profile["bio"] if patch["bio"] is MISSING else patch["bio"],
            "email": profile["email"]
            if patch["email"] is MISSING
            else patch["email"],
        }

    profile_from_db: dict[str, str | None] = {
        "name": "J. Doe",
        "bio": "Data Scientist",
        "email": "jane@example.com",
    }
    patch = parse_patch({"name": "jane", "bio": None})
    assert patch == {
        "name": "jane",  # -> user edited field
        "bio": None,  # -> user cleared field
        "email": MISSING,  # -> not sent in the form
    }
    print(f"{patch=}")
    updated_profile = apply_patch(profile_from_db, patch)
    assert updated_profile == {
        "name": "jane",
        "bio": None,
        "email": "jane@example.com",
    }
    print(f"{updated_profile=}")
    print("-" * 35)

    assert deepcopy(patch)["email"] is MISSING
    assert pickle.loads(pickle.dumps(patch))["email"] is MISSING  # noqa: S301
    print("=" * 50)


def part_4_sentinel_stop_loop() -> None:
    """Illustrate how to stop a loop without collisions."""

    def producer() -> Generator[str | DONE]:
        """Produce strings sending the sentinel "done" as end of stream."""
        yield "ready"
        yield "done"
        yield "pending"
        yield DONE

    for word in producer():
        if word is DONE:
            print(">>END OF STREAM: processing finished!")
            break
        print(f"Processing: {word=}")


def main() -> None:
    """Application entry point."""
    part_1_hello_sentinel_basics()
    print()

    part_2_sentinel_for_missing_values()
    print()

    part_3_sentinel_safe_to_copy()
    print()

    part_4_sentinel_stop_loop()
    print()


if __name__ == "__main__":
    main()
