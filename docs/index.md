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