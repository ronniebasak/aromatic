# Aromatic
ArangoDB Modelling Layer based on Pydantic and inspired by Odmantic


## Reached version 0.0.2 - Baby Steps
It now supports all of the following types
* `str`
* `int`
* `List`
* `Tuple`
* Naive `datetime`
* Naive `date`

### v0.0.3 - Objective - Jun 27
it now supports CRUD on the following types

* Work on the following types
    * Embedded Models (are simply Pydantic BaseModels, likely to change to accomodate invalid name error)
    * `List`
    * `Dict`
    * `datetime`
    * `date`
    * `Any`
    * `con*` types from pydantic

See `main.py` for usage. 


## Running Integration Tests (units coming soon)

### Setting up ArangoDB for Integration Tests
1. By default, expecting ArangoDB to be running at `http://localhost:8529/` 
```python
HOSTS = "http://localhost:8529"
USERNAME = "root"
PASSWORD = "openSesame"
DATABASE = "romatic_test"
```
2. To start a docker container with default credentials 

```shell
docker run --name arango -d -p 8529:8529 -e ARANGO_ROOT_PASSWORD=openSesame arangodb/arangodb:latest
```

3. Navigate to `http://localhost:8529` on your browser, login with set credentials
1. Select DB `_system`, on the left hand pane, select `Databases` > `Add Database` and create a new DB
   (we expect it to be `romatic_test` but if you want to change, feel free to do so)
   
1. In case the credentials, host, port and database varies in your system, feel free to set that in `test/conftest.py`


### Running the Tests

**To run Integration tests, cd into the git directory**
```shell
pytest -v
```

**To check coverage report**
```shell
coverage run -m pytest -v
coverage report
```

```text
Name                    Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------
aromatic/__init__.py        0      0      0      0   100%
aromatic/basemodel.py      20      0      8      0   100%
aromatic/engine.py        145     61     76      7    48%
aromatic/errors.py         19      9      6      0    40%
---------------------------------------------------------
TOTAL                     184     70     90      7    53%

```

*It is **strongly** advised that you take appropriate precautions when going outside due to covid. And do not run on
production if you're not willing to fix a lot of bugs.*