---
title: Overview
layout: post
---

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
