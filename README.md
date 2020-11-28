# Python MongoDB Runner

This module spins up a MongoDB background process programmatically.  This is quite helpful for testing when a real MongoDB instance is desired instead of mocking one.  Using the system's installed `mongod` executable, the process is launched using a temporary directory for the db storage.  The connection string to the running process can then be obtained and used to connect via your favorite MongoDB Client (e.g. pymongo or motor).

The idea is straight from [mongodb-memory-server](https://github.com/nodkz/mongodb-memory-server).  I've used it heavily for JS/TS development but haven't found a similar package for Python.  The idea would be for this package to eventually replicate their entire feature set.  (i.e. the automated downloading and utilization of mongodb binaries instead of relying on an existing system install)

## Installation

Install from source for now.  There are no external dependencies required.

```
git clone https://github.com/albalkum/python-mongodb-runner.git
cd python-mongodb-runner
pip install -e .
```

## Usage

Obtaining the connection URI is as easy as:

```python
from python-mongodb-runner import MongoRunner


runner = MongoRunner()
uri = runner.get_uri()
```

The URI can now be used with pymongo/motor.  E.g.

```python
client = pymongo.MongoClient(uri)
```

Boom.  Done.

The runner will automatically clean up the db (i.e. deleting the temporary db files) process exist (the destructor gets called) or manually calling `MongoRunner.close()`.  If a persistent database is desired, a directory `Path` argument is required.  When provided the data will not be deleted.

```python
from python-mongodb-runner import MongoRunner
from pathlib import Path


runner = MongoRunner(data_directory=Path('path/to/some/directory/that/exists'))
uri = runner.get_uri()
```

## TODOs

* Utilization of mongodb binaries similar to [mongodb-memory-server](https://github.com/nodkz/mongodb-memory-server)
* Better documentation