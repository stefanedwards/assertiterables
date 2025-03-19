# Hatch Demo

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-demo.svg)](https://pypi.org/project/hatch-demo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-demo.svg)](https://pypi.org/project/hatch-demo)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install hatch-demo
```

## License

`hatch-demo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Tips and tricks for developing

The package uses `pytest` for unit testing together with codecoverage, 
see section `[tool.pytest.ini_options]` in `pyproject.toml`.

### VS Code

`pyproject.toml` includes a number of settings for `pytest`, which are also
used when running the interactive debugger in VS code.

Add following to your `settings.json`, to avoid running code coverage that 
prevents the interactive debugger from working:

```json
"python.testing.pytestArgs": [ 
        "--import-mode=importlib",
        "--no-cov"
    ],
```
