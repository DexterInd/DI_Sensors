# Publishing to PyPI / TestPyPI

## Prerequisites

```bash
pip install build twine
```

You will need API tokens from:
- **TestPyPI**: https://test.pypi.org/manage/account/token/
- **PyPI**: https://pypi.org/manage/account/token/

Store them in `~/.pypirc` (never commit this file):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-<your-pypi-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-<your-testpypi-token>
```

## Step 1 — bump the version

Edit `version` in `pyproject.toml` before every release:

```toml
version = "0.0.0"
```

## Step 2 — build the distribution

From the `Python/` directory:

```bash
cd DI_Sensors/Python
python -m build
```

This produces two files in `dist/`:
- `di_sensors-2.0.0.tar.gz` — source distribution
- `di_sensors-2.0.0-py3-none-any.whl` — wheel

## Step 3 — publish to TestPyPI first

```bash
twine upload --repository testpypi dist/*
```

Verify the install from TestPyPI:

```bash
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  mr-di-sensors==0.0.0
python -c "import di_sensors; print('ok')"
```

> **Note:** `mr_rfr-tools` (a dependency) must already be available. If testing
> against TestPyPI only, publish `mr_rfr-tools` first and use `--extra-index-url`
> so pip can locate it.

## Step 4 — publish to PyPI

Once satisfied:

```bash
twine upload dist/*
```

The package is then installable on any Pi with:

```bash
pip install mr-di-sensors
```

## Cleanup

```bash
rm -rf dist/ build/ *.egg-info
```
