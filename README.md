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
