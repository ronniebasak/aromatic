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

