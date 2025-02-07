---
title: BODS for Linked Data
layout: post
---

# Introduction

This documentation describes how the [Beneficial Ownership Data Standard (BODS) version 0.4](https://standard.openownership.org/en/0.4.0/) data model can be interpreted and used as RDF, so that beneficial ownership data can be published as or converted to linked data. We assume you're already familiar with BODS 0.4 and the basics of RDF. We use [turtle syntax](https://www.w3.org/TR/turtle/) for RDF examples.

We explain when and why the RDF data model deviates from the JSON representation of BODS, and also describe as far as possible mappings to existing RDF terms and vocabularies. 

## Overview

The core BODS data model is represented in RDF by the following classes:

* `Statement` (with subclasses for new, updated, and closed record statements)
* `Declaration`
* `RecordDetails` (with subclasses for `Person`, `Entity`, `Relationship` and `Unspecified` records)
* `Interest` (with subclasses for the different `Interest` types)

Instances of the following classes are defined in line with the codelists in the data standard:

* `EntityType`
* `EntitySubtype`
* `PersonType`

Classes, subclasses and instances are also defined for the other components needed:

* `Address`
* `Agent`
* `Annotation`
* `Identifier`
* `Jurisdiction`
* `Name`
* `PoliticalExposure`
* `SecuritiesListing`
* `Source`
