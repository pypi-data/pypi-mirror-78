# atompack
A flexible Python library for atomic structure generation.
https://seatonullberg.github.io/atompack/

## Installation

### Download from [PyPI](https://pypi.org/project/atompack/)

This is the best method for end users.

```bash
$ python3 -m pip install atompack
```

### Build from source

This is the best method for contributors or anyone who is interested in modifying the code.

#### 1. Clone the source code with `git`:

```bash
$ git clone https://github.com/seatonullberg/atompack.git
$ cd atompack
```

#### 2. Compile the C extensions:

```bash
$ python3 setup.py build_ext --inplace
```

The following steps can be done with either `pipenv` or `pip`. I recommend using `pipenv`. If you're not familiar with the benefits of using `pipenv`, educate yourself here: https://pipenv-fork.readthedocs.io/en/latest/.

#### 3. Download the dependencies and install as editable:

For `pipenv` users:

```bash
$ pipenv install --dev
```

For `pip` users:

```bash
$ python3 -m pip install -e . [dev]
```

#### 4. Verify that all tests pass:

For `pipenv` users:

```bash
$ pipenv run pytest --doctest-modules -v ./atompack ./tests
```

For `pip` users:

```bash
$ python3 -m pytest --doctest-modules -v ./atompack ./tests
```

All done!