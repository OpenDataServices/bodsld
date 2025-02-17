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
* `PEPStatus`
* `PoliticalExposure`
* `SecuritiesListing`
* `SecuritiesIdentifier`
* `Source`

![A diagram showing the whole core data model](assets/diagrams/whole_core.png)

![A diagram showing the all the components of the data model](assets/diagrams/whole_components.png)
