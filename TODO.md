# Aromatic Roadmap

## Target for Version 0.0.1

### v0.0.1 - Proof of Concept
* Get a pydantic model to save to arangoDB as a document in a collection
* Get the same pydantic model to load from ArangoDB from the collection

### v0.0.2 - Baby Steps
* Work on the following types 
    * `str`
    * `int`
    * `List`
    * `Tuple`
    * Naive `datetime`
    * Naive `date`
    
### v0.0.3 - Objective
* Work on the following types
    * Embedded Models
    * `List`
    * `Dict`
    * `datetime`
    * `date`
    * `Any`
    * `con*` types from pydantic

### v0.0.4 - Graphic and Testing
* Work on defining `EdgeCollections` modelling
* Both uni and bidirectional.
* Write unit tests for all of them
* From this point onwards everything should be tested and follow TDD.

### v0.0.5 - Defining a usable API for document CRUD
* Basic Querying with operators and logic
* Save one 
* Bulk save
* Update one
* Bulk update
* Delete one
* Bulk delete

### v0.0.6 - Defining a usable API for Edge CRUD
* Basic Querying with operators and logic
* Save one
* Bulk save
* Update one
* Bulk update
* Delete one
* Bulk delete

### v0.0.7 - Joins and References
* Solve for joins and references
* Handle circular references.

### v0.0.8 - Indexes
* Define indexes
* Define API to initialize/apply/verify indexes via the model

### v0.0.9 - Documentation
* Write a example codes under various scenarios
* Document everything

### v0.0.10 - Advanced Query Engine
* Details are not clear at this moment
* But as much as possible things should be pythonic