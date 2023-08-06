# A Python interface to tmLQCD for Lyncs

[![python](https://img.shields.io/pypi/pyversions/lyncs_tmLQCD.svg?logo=python&logoColor=white)](https://pypi.org/project/lyncs_tmLQCD/)
[![pypi](https://img.shields.io/pypi/v/lyncs_tmLQCD.svg?logo=python&logoColor=white)](https://pypi.org/project/lyncs_tmLQCD/)
[![license](https://img.shields.io/github/license/Lyncs-API/lyncs.tmLQCD?logo=github&logoColor=white)](https://github.com/Lyncs-API/lyncs.tmLQCD/blob/master/LICENSE)
[![build & test](https://img.shields.io/github/workflow/status/Lyncs-API/lyncs.tmLQCD/build%20&%20test?logo=github&logoColor=white)](https://github.com/Lyncs-API/lyncs.tmLQCD/actions)
[![codecov](https://img.shields.io/codecov/c/github/Lyncs-API/lyncs.tmLQCD?logo=codecov&logoColor=white)](https://codecov.io/gh/Lyncs-API/lyncs.tmLQCD)
[![pylint](https://img.shields.io/badge/pylint%20score-9.4%2F10-green?logo=python&logoColor=white)](http://pylint.pycqa.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=codefactor&logoColor=white)](https://github.com/ambv/black)


[tmLQCD] is the simulation library used by the Extended Twisted Mass Collaboration (ETMC).
tmLQCD is a freely available software suite providing a set of tools to be used in lattice QCD
simulations. This is mainly a (P/R)HMC implementation for Wilson and Wilson twisted mass fermions
and inverter for different versions of the Dirac operator.

The code is fully parallelised and ships with optimisations for various modern architectures,
such as commodity PC clusters and the Blue Gene family.

[tmLQCD]: https://github.com/etmc/tmLQCD


## Installation

The package can be installed via `pip`:

```
pip install [--user] lyncs_tmLQCD
```

### External dependencies

For compiling tmLQCD, a fortran compiler, flex, openblas and lapack are required.

These can be installed via `apt`:

```
apt install -y flex libopenblas-dev liblapack-dev gfortran
```

OR using `conda`:

```
conda install -c anaconda openblas
conda install -c conda-forge flex lapack fortran-compiler
```

## Documentation

## Contributing

When contributing to the package, clone the source from [github](https://github.com/Lyncs-API/lyncs.tmLQCD):

```
git clone https://github.com/Lyncs-API/lyncs.tmLQCD
cd lyncs.tmLQCD
```

install the package in development mode:

```
pip install -e .[all]
```

and run the test-suite for checking the correctness of the installation:

```
pytest -v
```

If everything goes well, you should see all the tests passed and obtain a coverage report.

A main implementation requirement is an **high code-coverage**.
If you are going to implement something new, please, also add the respective
test files or functions in the `test/` directory.

Another implementation requirement is to **format the code** via [black](https://github.com/ambv/black)
and to use [pylint](https://github.com/PyCQA/pylint) for improving the code standard.

These packages can be installed via pip:

```
pip install black pylint
```

Before any commit, run black from the source directory:

```
black .
```

When you are done with the implementation, try to resolve as many comments/warnings/errors
as possible brought up by `pylint`:

```
pylint lyncs_tmLQCD
```

**NOTE:** pylint and black are incompatible in few formatting assumptions. Please, ignore
the comments C0303 and C0330 of pylint. If they show up in the files you have edited/added,
please, add the following line after the documentation string at the beginning of the respective files:

```
# pylint: disable=C0303,C0330
```

