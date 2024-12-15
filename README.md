# Rachadez API

## Setup
First, you'll need to setup your environment so that you can execute and build the project correctly. To do this, will need to install the [Poetry](https://python-poetry.org/docs/#installation) - the python package manager that will be used - to build the project and manage deps.

## Running
To run the application execute
```bash
make run-dev
```

Now, check `localhost:5001/` in your web browser or via command line with
```bash
curl localhost:5001/
<p>Hello World!</p>
```