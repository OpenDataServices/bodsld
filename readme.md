# BODS-LD

A script for convering the Beneficial Ownership Data Standard v0.4 into an RDF vocabulary, so BODS data can be used as linked data.

## Use

Check out the repo.

Create a virtual environment, or run in a docker container.

```
$ docker build --tag odsc/bodsld .
$ docker run -it --name bodsld -v /path/to/code/bodsld:/bodsld odsc/bodsld /bin/bash
```

All it does at the moment is fetch the JSON schema files from the BODS github repo, then runs a partly artisanal process to convert them to RDF turtle. It generates HTML documentation for the ontology using pyLODE.

```
$ python bodsld.py
```

Details of the mapping can be found ...