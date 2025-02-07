---
title: Vocabulary
layout: post
---

We define the following prefixes as part of our vocabulary

```
bods: https://vocab.openownership.org/terms#
codes: https://vocab.openownership.org/codelists#
orgid: https://org-id.guide/list/
```

The RDF vocabulary is available in full:

* In turtle format 
* As a JSON-LD context (TODO)

## Mapping to other terms

Reusing vocabularies is generally best practice when publishing RDF, however in terms of keeping the RDF data model and JSON data models for BODS aligned as closely as possible, we suggest defining all of our terms in the BODS vocabulary and aliasing them to existing terms where appropriate.

The following terms in BODS are aliases of `foaf:primaryTopic`:

* `declarationSubject`
* `recordDetails`

Further research is needed for a comprehensive mapping to existing vocabularies. Some examples include:

Address properties align with the [vcard vocabulary](https://www.w3.org/TR/vcard-rdf/).
Entity types in the [Follow The Money](https://followthemoney.tech/) data model.
Research to determine if country or jurisdiction codes have been published as RDF.

