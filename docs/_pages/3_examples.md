---
title: Examples
layout: post
---

```json
@prefix stmt: <https://example.org/statements/> .
@prefix rec: <https://example.org/records/> .
@prefix decl: <https://example.org/declarations/> .
@prefix bods: <https://vocab.openownership.org/terms#> .

_:gb a bods:Jurisdiction;
	bods:jurisdictionName "United Kingdom";
	bods:code "GB" .

_:pub1 bods:publisherName "Profitech Ltd" .

_:declaration1 a bods:Declaration;
	bods:declarationSubject rec:c359f58d2977 .

_:id1 a bods:Identifier;
    	bods:scheme "GB-COH";
    	bods:idString "2063384560" .

stmt:1dc0e987-5c57-4a1c-b3ad-61353b66a9b7
{
	stmt:1dc0e987-5c57-4a1c-b3ad-61353b66a9b7 a bods:NewRecordStatement;
        	bods:statementDate "2020-03-04"^^xsd:dateTime;
        	bods:publicationDate "2020-03-04"^^xsd:dateTime;
        	bods:version "0.4";
        	bods:publisher _:pub1;
        	bods:recordDetails rec:c359f58d2977 .

	rec:c359f58d2977 a bods:Entity;
    	   	bods:recordIdString "c359f58d2977";
    	   	bods:entityType bods:RegisteredEntity;
    	   	bods:entityName "Profitech Ltd";
    	   	bods:foundingDate "2019-09-03"^^xsd:dateTime;
    	   	bods:identifier _:id1 .

}

_:name1 a bods:LegalName;
	bods:fullName "Jennifer Hewitson-Smith";
	bods:giveName "Jennifer";
	bods:familyName "Hewitson-Smith" .

_:name2 a bods:AlternativeName;
	bods:fullName "Jenny Hewitson-Smith" .

_:addr1 a bods:ServiceAddress;
	bods:address "76 York Road Bournemouth";
	bods:postCode "BH81 3L0";
	bods:country _:gb .

stmt:019a93f1-e470-42e9-957b-03559861b2e2
{
	stmt:019a93f1-e470-42e9-957b-03559861b2e2 a bods:NewRecordStatement;
    	bods:statementDate "2020-03-04"^^xsd:dateTime;
    	bods:publicationDate "2020-03-04"^^xsd:dateTime;
    	bods:version "0.4";
    	bods:publisher _:pub1;
    	bods:recordDetails rec:10478c6cf6de .

	rec:10478c6cf6de a bods:Person;
    	bods:personType bods:KnownPerson;
    	bods:nationality _:gb;
    	bods:personName _:name1, name2;
    	bods:birthDate "1978-07"^^xsd:dateTime;
    	bods:address _:addr1 .
}

stmt:fbfd0547-d0c6-4a00-b559-5c5e91c34f5c
{
	stmt:fbfd0547-d0c6-4a00-b559-5c5e91c34f5c a bods:NewRecordStatement;
    	bods:statementDate "2020-03-04"^^xsd:dateTime;
    	bods:publicationDate "2020-03-04"^^xsd:dateTime;
    	bods:version "0.4";
    	bods:publisher _:pub1;
    	bods:recordDetails rec:93b53022ae6a .

	rec:93b53022ae6a a bods:Relationship;
    	bods:subject rec:c359f58d2977;
    	bods:interestedParty rec:10478c6cf6de;
    	bods:interest _:interest1 .

	_:interest1 a bods:Interest;
    	bods:interestType bods:Shareholding;
    	bods:beneficialOwnershipOrControl "true"^^xsd:boolean;
    	bods:startDate "2016-04-06"^^xsd:dateTime;
    	bods:shareExact "100" .
}

```