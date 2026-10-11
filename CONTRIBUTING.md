# Contributing to muxpy

Thank you for considering contributing to **muxpy**! 🎉  
We welcome bug reports, feature requests, documentation improvements, and code contributions.

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Adding a New Termux API Module](#adding-a-new-termux-api-module)

---

## Code of Conduct

Please be respectful. This is an open and welcoming community. Harassment or discriminatory behavior of any kind will not be tolerated.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/muxpy.git
   cd muxpy
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feat/my-new-feature
   ```

---

## Development Setup

muxpy has **zero runtime dependencies**. Only dev tools are needed:

```bash
pip install -e ".[dev]"
```

This installs the library in editable mode along with `pytest` and `pytest-asyncio`.

---

## Running Tests

The full test suite runs via Python's built-in `unittest` (no extra dependencies required):

```bash
# Standard (no pytest)
python -m unittest discover tests

# With pytest (if installed)
pytest
```

> All tests run entirely in **mock mode** — no Android device required.

---

## Submitting Changes

1. Ensure all tests pass: `python -m unittest discover tests`
2. Update `CHANGELOG.md` under the `[Unreleased]` section.
3. Open a **Pull Request** against the `main` branch.
4. In the PR description, describe what you changed and why.

---

## Coding Standards

- **Python 3.9+** compatible syntax only.
- **Type annotations** required on all public functions.
- **Docstrings** (Google or plain style) on all classes and public methods.
- Line length: max **100 characters**.
- Run `ruff check src/` before submitting (if ruff is available).

---

## Adding a New Termux API Module

To wrap a new `termux-*` command, follow this pattern:

1. Create a new file: `src/muxpy/api/your_module.py`
2. Define a typed dataclass for the return value (if the command returns structured data).
3. Create a class `YourApi(...)` with an `AsyncExecutor` in the constructor.
4. Add mock defaults in `src/muxpy/core/executor.py` → `_default_mock_json()`.
5. Register the new API on `TermuxClient` in `src/muxpy/client.py`.
6. Export the dataclass from `src/muxpy/__init__.py`.
7. Write at least one test case in `tests/test_client.py`.
8. Document the API in `README.md` under the API Reference table.
