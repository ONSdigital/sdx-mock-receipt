# sdx-mock-receipt

The sdx-mock-receipt service is used within the Office for National Statistics (ONS) for mocking the Survey Data Exchange (SDX) Receipting service.

## Installation
This application presently installs required packages from requirements files:
- `requirements.txt`: packages for the application, with hashes for all packages: see https://pypi.org/project/hashin/
- `test-requirements.txt`: packages for testing and linting

It's also best to use `pyenv` and `pyenv-virtualenv`, to build in a virtual environment with the currently recommended version of Python.  To install these, see:
- https://github.com/pyenv/pyenv
- https://github.com/pyenv/pyenv-virtualenv
- (Note that the homebrew version of `pyenv` is easiest to install, but can lag behind the latest release of Python.)

### Getting started
Once your virtual environment is set, install the requirements:
```shell
$ make build
```

To test, first run `make build` as above, then run:
```shell
$ make test
```

It's also possible to install within a container using docker. From the sdx-mock-receipt directory:
```shell
$ docker build -t sdx-mock-receipt .
```

## Usage

Start sdx-mock-receipt service using the following command:

```shell
$ python server.py
```

or:
```shell
$ make start
```

If you've built the image under docker, you can start using the following:
```shell
$ docker run -p 5000:5000 sdx-mock-receipt
```

sdx-mock-receipt exposes one endpoint:
  - '/receipts'
    - This simply returns 201 and "status": "ok" when it receives a HTTP POST request.

By default this service binds to port 5000 on localhost.

## Linting

To run flake8 against the repo, use:
```bash
$ make test
```
