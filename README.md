# Aromatic
ArangoDB Modelling Layer based on Pydantic and inspired by Odmantic


# Reached version 0.0.1 - Proof of Concept
It has been possible to load and save pydantic models via this API.

* `engine.save(Model)` saves into the model
* `engine.find(Model, query)` return a list
* `engine.find_one(Model, query)` returns a single model 