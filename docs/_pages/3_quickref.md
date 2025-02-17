---
title: Quick Reference
layout: post
---

This is a list of the changes for each JSON object type and its properties that need to be made when transforming from the [JSON data model](https://standard.openownership.org/en/0.4.0/standard/schema-browser.html) to the RDF data model.

Where the value of a property is a nested object in JSON, unless otherwise stated, this object is converted into an instance with a relevant `rdf:type` value, and the value of the property is the URI of this instance (or blank node identifier).

For more detail about the differences, see the Data Model documentation.

## Core

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
* `interests`: becomes `interest`; the value goes from a nested object to the URI of an instance.

### UnspecifiedRecord

In JSON we use a nested object to describe an unspecified person or entity. This is replaced with the `UnspecifiedRecord` class which is a subclass of `RecordDetails` (like `Person` and `Entity`).

* `reason`: renamed to `unspecifiedReason`; value is an instance from the codelist.
* `description`: renamed to `unspecifiedDescription`.

### Interest

* `type`: removed; use a `rdf:type` with a class.
* `directOrIndirect`: unchanged; value is an instance from the codelist.
* `beneficialOwnershipOrControl`: unchanged.
* `details`: unchanged.
* `share`: removed; nested properties are flattened to `shareExact`, `shareMaximum`, `shareExclusiveMinimum`, `shareExclusiveMaximum`.
* `startDate`: unchanged.
* `endDate`: unchanged.

## Components

### Address

* `type`: removed; use a `rdf:type` with a class.
* `address`: renamed to `streetAddress`.
* `postCode`: unchanged.
* `country`: unchanged, but the value is a [`Jurisdiction`](#jurisdiction).

### Annotation

* `statementPointerTarget`: unchanged.
* `creationDate`: unchanged.
* `createdBy`: value is an `Agent` instance.
* `motivation`: unchanged; value is an instance from the codelist.
* `description`: unchanged.
* `transformedContent`: unchanged.
* `url`: unchanged.

### Country

Removed and replaced with [`Jurisdiction`](#jurisdiction) throughout.

### Identifier

* `id`: renamed to `idString`.
* `scheme`: unchanged.
* `schemeName`: unchanged.
* `uri`: unchanged.

### Jurisdiction

* `name`: renamed to `jurisdictionName`.
* `code`: unchanged.

### Name

* `type`: removed; use a `rdf:type` with a class.
* `fullName`: unchanged.
* `familyName`: unchanged.
* `givenName`: unchanged.
* `patronymicName`: unchanged.

### PEPstatusDetails

Renamed to `PoliticalExposure`.

* `reason`: renamed to `pepStatusReason`.
* `missingInfoReason`: unchanged.
* `jurisdiction`: renamed to `pepJurisdiction`.
* `startDate`: unchanged.
* `endDate`: unchanged.
* `source`: unchanged.

### PublicListing

Removed and flattened onto [`Entity`](#record-details-entity) (nested property names unchanged, except for `companyFilingsURLs` which becomes `companyFilingsURL`).

### PublicationDetails

Removed and flattened onto [`Statement`](#statement).

### Publisher

Renamed to `Agent` for use in other places.

* `name`: unchanged.
* `url`: renamed to `uri`.

### SecuritiesListing

* `marketIdentifierCode`: unchanged.
* `operatingMarketIdentifierCode`: unchanged.
* `stockExchangeJurisdiction`: unchanged.
* `stockExchangeName`: unchanged.
* `security`: renamed to `securityId`; convert the nested object into an instance of `SecuritiesIdentifier` (which is a subclass of [`Identifier`](#identifier) with the additional property of `ticker`).

### Share

Removed and flattened onto [`Interest`](#interest). Note property names are prefixed with `share*` for clarity.

### Source

* `type`: removed; use a `rdf:type` with a class.
* `description`: unchanged.
* `url`: unchanged.
* `retrievedAt`: unchanged.
* `assertedBy`: nested object is replaced with `Agent` instance.

## Codelists

Where codelists are converted into instances, capitalise the code and prefix it with the namespace `https://vocab.openownership.org/codelists#` (prefixed `codes:`) to create a URI. Use this URI as the value where a string of the code would be used in the JSON format. The following codelists are part of the vocabulary as instances:

* `annotationMotivation`: values become instances of the `AnnotationMotivation` class
* `directOrIndirect`: values become instances of the `DirectOrIndirect` class
* `entityType`: values become instances of the `EntityType` class
* `entitySubtype`: values become instances of the `EntitySubtype` class
* `personType`: values become instances of the `PersonType` class
* `securitiesIdentifierSchemes`: values become instances of `SecuritiesIdentifierScheme` class
* `unspecifiedReason`: values become instances of the `UnspecifiedReason` class

Where codelists are converted into classes, capitalise the code and prefix it with the namespace `https://vocab.openownership.org/terms#` (prefixed `bods:`) to create a URI. Use this as the `rdf:type` value for an instance which, as a JSON object, would have had a property pointing to the string of the code. The following codelists are part of the vocabulary as classes:

* `addressType`: the values become subclasses of `Address`
* `interestType`: the values become subclasses of `Interest`
* `nameType`: the values become subclasses of `Name`
* `recordStatus`: the values `new`, `updated` and `closed` are converted to `NewRecordStatement`, `UpdatedRecordStatement` and `ClosedRecordStatement` respectively, as subclasses of `Statement`.
* `recordType`: the values become as subclasses of `RecordDetails`.
* `sourceType`: the values become subclasses of `Source`
