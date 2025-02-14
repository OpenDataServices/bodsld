---
title: Converting data
layout: post
---

BODS v0.4 JSON data can be converted to RDF in line with the data model described here.

While the code in this repository converts the _schema_ into an RDF vocabulary, it may serve as a useful starting point for any _data_ conversion scripts.

## Summary of changes

This is a list of the changes for each JSON object type and its properties that need to be made when transforming from the [JSON data model](https://standard.openownership.org/en/0.4.0/standard/schema-browser.html) to the RDF data model.

Where the value of a property is a nested object in JSON, unless otherwise stated, this object is converted into an instance with a relevant `rdf:type` value, and the value of the property is the URI of this instance (or blank node identifier; see the Data Model documentation).

### Statement

* `statementId`: renamed to `statementIdString`; and the value is used for the URI for the `Statement` instance.
* `statementDate`: unchanged.
* `annotations`: becomes `annotation`.
* `publicationDetails`: removed; nested properties are flattened so `bodsVersion`, `license`, `publicationDate` and `publisher` are on the Statement. Value of `publisher` is an `Agent`.
* `source`: unchanged.
* `declaration`: value is a `Declaration` instance.
* `declarationSubject`: moved to `Declaration` instance.
* `recordId`: moved to a `RecordDetails` instance and renamed to `recordIdString`; and the value is used for the URI of the `RecordDetails` instance.
* `recordType`: removed; use to generate the `rdf:type` value for the `RecordDetails` instance.
* `recordStatus`: removed; use to generate the `rdf:type` value for the `Statement` instance.
* `recordDetails`: the value is the URI of a `RecordDetails` instance.

### Record details (entity)

These go from a nested object under `recordDetails` on `Statement` to an instance with an `rdf:type` of `Entity`.

* `isComponent`: removed.
* `entityType`: value is an instance of an `EntityType` (generated from the entityType codelist).
* `entityType/subtype`: flattened to `entitySubtype`; value is an instance of an `EntitySubtype` (generated from the entitySubtype codelist).
* `entityType/details`: flattened to `entityTypeDetails`.
* `unspecifiedEntityDetails`: removed; use an instance of `UnspecifiedRecord` instead.
* `name`: unchanged.
* `alternateNames`: becomes `alternateName`.
* `jurisdiction`: unchanged.
* `identifiers`: becomes `identifier`.
* `foundingDate`: unchanged.
* `dissolutionDate`: unchanged.
* `addresses`: becomes `address`.
* `uri`: unchanged.
* `publicListing`: removed; nested properties are flattened to `hasPublicListing`, `companyFilingsURL` and `securitiesListing`.
* `formedByStatute`: removed; nested properties are flattened to `formedByStatuteName` and `formedByStatuteDate`.

### Record details (person)

These go from a nested object under `recordDetails` on `Statement` to an instance with an `rdf:type` of `Person`.

* `isComponent`: removed.
* `personType`: value is an instance of a `PersonType` (generated from the personType codelist).
* `unspecifiedPersonDetails`: removed; use an instance of `UnspecifiedRecord` instead.
* `names`: becomes `name`.
* `identifiers`: becomes `identifier`.
* `nationalities`: becomes `nationality`.
* `placeOfBirth`: unchanged.
* `birthDate`: unchanged.
* `deathDate`: unchanged.
* `taxResidencies`: becomes `taxResidency`.
* `addresses`: becomes `address`.
* `politicalExposure`: value is the identifier for a `PoliticalExposure` instance.
* `politicalExposure/status`: replaced with `pepStatus`, the value for which is an instance of `PEPStatus`.

### Record details (relationship)

These go from a nested object under `recordDetails` on `Statement` to an instance with an `rdf:type` of `Relationship`.

* `isComponent`: removed.
* `componentRecords`: removed.
* `subject`: the value goes from a recordId string to the URI of an instance.
* `interestedParty`: the value goes from a recordId string to the URI of an instance.
* `intersts`: becomes `interest`; the value goes from a nested object to the URI of an instance.
