# BODS-LD

This repo contains the latest version of the RDF vocabulary as generated from the current (v0.4.0) schema (`docs/terms/bods-vocabulary-0.4.0.ttl`) and equivalent HTML documentation (`docs/terms/bods-vocabulary-0.4.0.html`).

It also contains script for generating the vocabulary and documentation. This only needs to be run if there are changes to the schema, or to the mapping from the schema to the RDF data model.

## Mapping

See the documentation attached to this repo.

### Limitations

Most of the vocabulary is derived directly from the JSON Schema, which means it can be generated from versions of the schema translated into different languages. However, due to a few changes to the model, there are some customisations which will not be translated in this case, and will need to be adjusted by hand.

Instance data (eg. entity types, annotation motivations; other things from codelists) is included in the RDF but not in the HTML documentation due to a limitation of the library used to generate it.

## Use

Check out the repo.

Create a virtual environment, or run in a docker container.

```
$ docker build --tag odsc/bodsld .
$ docker run -it --name bodsld -v /path/to/code/bodsld:/bodsld odsc/bodsld /bin/bash
```

The script fetches the JSON schema files from the BODS github repo if they are not present locally, then runs a partly artisanal process to convert them to RDF turtle. It generates HTML documentation for the ontology using pyLODE.

```
$ python bodsld.py
```

The default file for the vocabulary is `bods-vocabulary-0.4.0.ttl` and the HTML documentation is `bodsvocab.html`. These file names can be changed at the end of the `bodsld.py` script if needed.

## Converting BODS data

This script currently maps the BODS _schema_ to an RDF _vocabulary_. It doesn't provide any way to convert _data_ between formats. However, it may be useful as a guideline for the mapping in future.
