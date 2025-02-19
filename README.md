# Rachadez API

## Setup
First, you'll need to setup your environment so that you can execute and build the project correctly. To do this, will need to install the [Poetry](https://python-poetry.org/docs/#installation) - the python package manager that will be used - to build the project and manage deps.

Once installed, run the command in project root dir
```bash
poetry install
```

## Running
To run the application execute
```bash
make run-dev
```

Now, check `localhost:8000/v1` in your web browser or via command line with
```bash
curl localhost:5001/
{ msg: Hello World! }
```
