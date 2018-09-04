# sdx-mock-receipt

The sdx-mock-receipt service is used within the Office for National Statistics (ONS) for mocking the Survey Data Exchange (SDX) Receipting service.

## Installation

Using virtualenv and pip, create a new environment and then install within using:

    $ pip install -r requirements.txt

or:

    $ make build

It's also possible to install within a container using docker. From the sdx-mock-receipt directory:

    $ docker build -t sdx-mock-receipt .

## Usage

Start sdx-mock-receipt service using the following command:

    python server.py

or:

    make start

If you've built the image under docker, you can start using the following:

    docker run -p 5000:5000 sdx-mock-receipt

sdx-mock-receipt exposes one endpoint:
  - '/receipts'
    - This simply returns 201 and "status": "ok" when it receives a HTTP POST request.

By default this service binds to port 5000 on localhost.

## Linting

To run flake8 against the repo, use:
```bash
    make test
```
