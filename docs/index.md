---
title: BODS for Linked Data
layout: post
---

# Introduction

This documentation describes how the [Beneficial Ownership Data Standard (BODS) version 0.4](https://standard.openownership.org/en/0.4.0/) data model can be interpreted and used as RDF, so that beneficial ownership data can be published as or converted to linked data. We assume you're already familiar with BODS 0.4 and the basics of RDF. We use [turtle syntax](https://www.w3.org/TR/turtle/) for RDF examples.

We explain when and why the RDF data model deviates from the JSON representation of BODS, and also describe as far as possible mappings to existing RDF terms and vocabularies. 

## Conversion script

The Python script in this repository converts the JSON schema to RDF. This is partially automated directly from the JSON, and contains some artisanal adjustments due to differences between the JSON data model and the RDF data model (which are explained in this documentation). The script also generates an HTML file of vocabulary documentation directly from the RDF using [pyLODE](https://github.com/RDFLib/pyLODE/).

As a user of the vocabulary you won't need to run the script, as the vocabulary (.ttl) file is also included in this repo and available via the docs site.

### Limitations

Most of the vocabularly is derived directly from the JSON Schema, which means it can be generated from versions of the schema translated into different languages. However, due to a few changes to the model, there are some customisations which will not be translated in this case, and will need to be adjusted by hand.

Instance data (eg. entity types, annotation motivations; other things from codelists) is included in the RDF but not in the HTML documentation due to a limitation of the library used to generate it.

### Use

If you do want to run the script, because the underlying schema has changed and you need to re-generate the RDF, or you want to modify the script for some other reason, you can check out the repo and run the a docker container (or ignore the docker steps and just run it in a virtual environment):

```
$ docker build --tag odsc/bodsld .
$ docker run -it --name bodsld -v /path/to/code/bodsld:/bodsld odsc/bodsld /bin/bash
```

The script fetches the JSON schema files from the BODS github repo if they are not present locally, then runs a partly artisanal process to convert them to RDF turtle. It generates HTML documentation for the ontology using pyLODE.

```
$ python bodsld.py
```

The default file for the vocabulary is `bods-vocabulary-0.4.0.ttl` and the HTML documentation is `bodsvocab.html`. These file names can be changed at the end of the `bodsld.py` script if needed.