# Aromatic
ArangoDB Modelling Layer based on Pydantic and inspired by Odmantic


## Reached version 0.0.1 - Proof of Concept
It has been possible to load and save pydantic models via this API.

* `engine.save(Model)` saves into the model
* `engine.find(Model, query)` return a list
* `engine.find_one(Model, query)` returns a single model

## Reached version 0.0.2 - Baby Steps
It now supports all of the following types
* `str`
* `int`
* `List`
* `Tuple`
* Naive `datetime`
* Naive `date`

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
```

```text
As of Jun 11, the integration tests have a 59% coverage

Name                    Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------
aromatic/__init__.py        0      0      0      0   100%
aromatic/basemodel.py      20      0      8      0   100%
aromatic/engine.py        122     43     64      7    55%
aromatic/errors.py         19      9      6      0    40%
---------------------------------------------------------
TOTAL                     161     52     78      7    59%

```

*It is **strongly** advised that you take appropriate precautions when going outside due to covid. And do not run on
production if you're not willing to fix a lot of bugs.*