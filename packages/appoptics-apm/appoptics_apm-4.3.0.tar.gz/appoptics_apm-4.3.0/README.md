[![Build Status](https://travis-ci.com/librato/python-appoptics.svg?token=hJPGuB4cPyioy5R8LBV9&branch=ci)](https://travis-ci.com/librato/python-appoptics)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/appoptics_apm?style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/appoptics_apm?style=plastic)
![PyPI](https://img.shields.io/pypi/v/appoptics_apm?style=plastic)

# appoptics_apm

The 'appoptics_apm' module provides automatic instrumentation and metrics/tracing SDK hooks for use with [AppOptics](https://appoptics.com).

The appoptics_apm module provides middleware and other instrumentation for popular web frameworks such as Django, Tornado, Pyramid, and WSGI, as well as commonly used libraries like SQLAlchemy, httplib, redis, memcached.  Read more at [our full documentation](https://docs.appoptics.com/kb/apm_tracing/python/).


## Installing

The Python instrumentation for AppOptics uses a module named `appoptics_apm`, which is distributed via pypi.

```sh
pip install appoptics_apm
```

Alternately, you can use this repository to build a local copy.

## Configuring

See our documentation on [configuring the python instrumentation](https://docs.appoptics.com/kb/apm_tracing/python/configure/).

# Upgrading

To upgrade an existing installation, you simply need to run:

```sh
pip install --upgrade appoptics_apm
```

## Running the Tests

Most of the test suite is configured to automatically run in Travis; there is also a way to run them locally in a Docker Compose environment.

### Test directory layout

All tests are under the `test` directory, top-level files such as `install_test_dependencies.sh` are shared by both Travis and Docker Compose to help set up test dependencies.  The actual test suite is organized into these subdirectories:

* `unit` -- these are actually functional tests; naming is for historic reasons.
* `extension` -- these are tests that exercise the actual c-lib extension, which is stubbed in the unit tests.
* `manual` -- manual verification of certain behaviors.
* `docker/install_tests.sh` -- these test installing the built agent distribution on a variety of platforms.

### Running the tests locally via docker-compose

#### Prerequisites

* install Docker and Docker Compose on your local machine

* have the built agent distribution under your local `dist/` directory

  Most of the tests depend on agent code in the local working tree but some, like the install tests, depend on having the distribution built and available locally.  There is a Dockerfile and helper script `run_docker_dev.sh` for this project that helps set up a development environment in which you can build the agent, see comments in `run_docker_dev.sh` for instructions.  Once in the development container, run `make sdist-package` to create a local agent distribution, then exit the container.  You should now have something like `dist/appoptics_apm-3.5.9.tar.gz`.

#### Run tests

Do this on your local machine, by going into the `test/docker` directory under this project.  This directory contains Docker Compose configuration and supporting files to help run the unit, extension, and install tests in a local composed environment.

For example, if the project is checked out under `~/source/python-appoptics`:
```
cd ~/source/python-appoptics/test/docker
```

To see the test matrix as defined by the Compose environment:
```
docker-compose config
```

To run the entire test suite:
```
docker-compose up -d
```

Test logs are written to `test/docker/logs`, and each composed service (i.e. test run) will exit 1 if there are test failures,  you can check via:
```
docker-compose ps
```

Once done, tear down via:
```
docker-compose down
```

See the comments in the `docker-compose.yml` file for more information.

#### Code Coverage Report for Tests

To activate code coverage reports for your tests, you can simply set the following environment variable in your shell:
```
PYTHON_APPOPTICS_CODECOVERAGE=1
```

This will measure your code coverage with the `coverage` Python module and create html-reports in the `test/docker/reports` directory for the unit as well as the extension tests. The reports will be stored under
```
<project_root>/test/docker/reports/<service>/<unit|extension>/index.html
````
and can simply be viewed with your browser.

For example, if the project is checked out under `~/source/python-appoptics`:

Run the desired service `<service>` with temporarily activated coverage measurement:
```
PYTHON_APPOPTICS_CODECOVERAGE=1 docker-compose up <service> -d
```

After the tests have been completed, you should find the coverage report for this service under
```
~/source/python-appoptics/test/docker/reports/<service>
```

To view e.g. the unit test results, just open
```
~/source/python-appoptics/test/docker/reports/<service>/unit/index.html
```
in your browser.

## Support

If you find a bug or would like to request an enhancement, feel free to file
an issue. For all other support requests, please email support@appoptics.com.

## Contributing

You are obviously a person of great sense and intelligence. We happily
appreciate all contributions to the appoptics_apm module whether it is documentation,
a bug fix, new instrumentation for a library or framework or anything else
we haven't thought of.

We welcome you to send us PRs. We also humbly request that any new
instrumentation submissions have corresponding tests that accompany
them. This way we don't break any of your additions when we (and others)
make changes after the fact.

### Activating Git hooks

This repo provides a folder hooks, in which all git hook related scripts can be found. Currently, there is only a pre-commit hook which runs Pylint on the changed \*.py files.

To set up the pre-commit hook, simply run the `install_hook.sh` script in this folder. This will install a project-specific virtual Python environment under which the code will be linted. Note that this requires Pyenv and Pyenv-virtualenv to be installed on your system.

Note:
Pyenv-virtualenv provides a functionality to automatically detect your project-specific virtual environment (e.g. when changing into the project folder in the terminal). To activate the auto-detection, you only need to make sure that you added `pyenv virtualenv-init` to your shell (refer to the installation section for [pyenv-virtualenv]( https://github.com/pyenv/pyenv-virtualenv) for more details).

### Pylint
To make sure that the code conforms the standards defined in the `.pylintrc` file, the pre-commit hook will not allow you to commit code if Pylint does issue any errors or warnings on the files you changed.

You can change this behaviour by setting certain environment variables when invoking `git commit`.

#### Ignore Pylint warning messages
You can commit your code even though Pylint issued warning messages by setting
```
PYTHON_APPOPTICS_PYLINT_IGNORE_WARNINGS=1
```
when invoking git commit.

#### Ignore Pylint error messages
You can commit your code even though Pylint issued error messages by setting
```
PYTHON_APPOPTICS_PYLINT_IGNORE_ERRORS=1
```
when invoking git commit. Please use this option with great care as Pylint error messages usually indicate genuine bugs in your code.

### Code Formatting with Yapf
For a more consistent formatting of the Python files, this repository comes with the code formatter Yapf pre-installed in the virtual environment. The configurations of Yapf are stored in the `.style.yapf` file in the root directory of this repository. Please consult the [Yapf documentation](https://github.com/google/yapf) for more information about the auto-formatter.

Currently, the formatting is not enforced through any commit hooks, but you can invoke Yapf with the provided configuration in your local development environment.

## Developer Resources

We have made a large effort to expose as much technical information
as possible to assist developers wishing to contribute to the AppOptics module.
Below are the three major sources for information and help for developers:

* The [AppOptics Knowledge Base](https://docs.appoptics.com/) has a large collection of technical articles or, if needed, you can submit a support request directly to the team.

If you have any questions or ideas, don't hesitate to contact us anytime.

To see the code related to the C++ extension, take a look in `appoptics_apm/swig`.

## License

Copyright (c) 2017 SolarWinds, LLC

Released under the [Librato Open License](http://docs.appoptics.com/Instrumentation/librato-open-license.html)
