from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, OWL, DCTERMS
from pylode.profiles.ontpub import OntPub

from helpers import *


BODS = Namespace("https://standard.openownership.org/terms#")
CODES = Namespace("https://standard.openownership.org/codelists#")
ORGID = Namespace("https://org-id.guide/list/")


class BODSVocab:

    def __init__(self, schema_files, codelists):

        self.registry = schema_registry(schema_files)
        self.schemas = schema_resources(schema_files)
        self.codelists = codelists

        self.exclude = []
        self.rename = []
        self.rename_map = {}
        self.date_props = []

        self.record_types = get_codes_and_info(self.codelists, "recordType.csv")
        
        self.g = Graph()
        self.g.bind("bods", BODS)
        self.g.bind("codes", CODES)
        self.g.bind("orgid", ORGID)

        count = len(self.schemas)
        print(f"Found {count} schemas.")

    def exclude_properties(self, exclude):
        self.exclude = exclude

    def rename_properties(self, rename, rename_map):
        self.rename = rename
        self.rename_map = rename_map

    def property_ranges(self, date_props, uri_props, name_props):
        self.date_props = date_props
        self.uri_props = uri_props
        self.name_props = name_props

    def metadata(self, uri, label, comment):
        ont_uri = URIRef(uri)
        self.g.add((ont_uri, RDF.type, OWL.Ontology))
        self.g.add((ont_uri, RDFS.label, Literal(label)))
        self.g.add((ont_uri, RDFS.comment, Literal(comment)))

    def map_class(self, classname, path):
        self.g.add((classname, RDF.type, OWL.Class))

        title = self.get_title(path)
        descr = self.get_description(path)
        # Special case for person/entity/relationship
        if title == None:
            if "relationship" in path:
                title = self.record_types.get("relationship")[0]
                descr = self.record_types.get("relationship")[1]
            if "person" in path:
                title = self.record_types.get("person")[0]
                descr = self.record_types.get("person")[1]
            if "entity" in path:
                title = self.record_types.get("entity")[0]
                descr = self.record_types.get("entity")[1]

        self.g.add((classname, RDFS.label, Literal(title)))
        self.g.add((classname, RDFS.comment, Literal(descr)))

    def map_properties(self, domain, path):
        properties = get_properties(self.registry, path)
        props = {}
        for p in properties:
            if p not in self.exclude:
                if "urn:" in path:
                    props[p] = f"/properties/{p}"
                else:
                    props[p] = f"{path}/properties/{p}"

        for prop, path in props.items():
            prop_range = self.get_property_range(path, prop)
            prop = self.rename_property(prop)

            title = self.get_title(path) or prop
            description = self.get_description(path) or prop
            self.g.add((BODS[prop], RDF.type, RDF.Property))
            self.g.add((BODS[prop], RDFS.domain, domain))
            self.g.add((BODS[prop], RDFS.label, Literal(title)))
            self.g.add((BODS[prop], RDFS.comment, Literal(description)))

            if prop_range:
                self.g.add((BODS[prop], RDFS.range, prop_range))

    def map_types(self, subclassof, bodstype, codelist):
        self.g.add((bodstype, RDF.type, OWL.Class))
        types = get_codes_and_info(self.codelists, codelist)
        
        for code in types:
            t = cap_first(code)
            self.g.add((BODS[t], RDF.type, OWL.Class))
            self.g.add((BODS[t], RDFS.subClassOf, subclassof))
            self.g.add((BODS[t], RDFS.label, Literal(types.get(code)[0])))
            self.g.add((BODS[t], RDFS.comment, Literal(types.get(code)[1])))

    def map_instances(self, instance_class, codelist):
        self.g.add((instance_class, RDF.type, OWL.Class))
        types = get_codes_and_info(self.codelists, codelist)
        
        for code, info in types.items():
            t = cap_first(code)
            self.g.add((BODS[t], RDF.type, instance_class))
            self.g.add((BODS[t], RDFS.label, Literal(types.get(code)[0])))
            self.g.add((BODS[t], RDFS.comment, Literal(types.get(code)[1])))


    def make_graph(self):
        # self.map_statement()
        # self.map_declaration()
        # self.map_record()
        self.map_person()
        # self.map_entity()
        # self.map_relationship()
        # self.map_unspecified()
        # self.map_interest()
        # self.map_address()
        # self.map_agent()
        # self.map_annotation()
        # self.map_jurisdiction()
        # self.map_identifier()
        # self.map_name()
        self.map_pepstatus()
        self.map_politicalexposure()

    def map_statement(self):
        path = "/$defs/Statement"
        self.map_class(BODS.Statement, path)

        # Turn recordStatus codelist into classes
        self.map_types(BODS.Statement, BODS.Statement, "recordStatus.csv")
        record_status = get_codes_and_info(self.codelists, "recordStatus.csv")

        # Statement properties
        self.map_properties(BODS.Statement, path)
        pd_path = "/$defs/Statement/properties/publicationDetails"
        self.map_properties(BODS.Statement, pd_path)

        # Range fixup
        # TODO: can I automate these ranges from the $ref?
        self.g.add((BODS.annotation, RDFS.range, BODS.Annotation))
        self.g.add((BODS.publisher, RDFS.range, BODS.Agent))
        self.g.add((BODS.source, RDFS.range, BODS.Source))
        self.g.add((BODS.recordDetails, RDFS.range, BODS.RecordDetails))

    def map_declaration(self):
        # Set label and description as these aren't in the JSON
        label = "Declaration"
        descr = "Each declaration is a set of claims about the entities, people and relationships within the subject’s beneficial ownership network."

        self.g.add((BODS.Declaration, RDF.type, OWL.Class))
        self.g.add((BODS.Declaration, RDFS.label, Literal(label)))
        self.g.add((BODS.Declaration, RDFS.comment, Literal(descr)))

        ## Declaration properties

        self.g.add((BODS.declarationIdString, RDF.type, RDF.Property))
        self.g.add((BODS.declarationIdString, RDFS.domain, BODS.Declaration))
        self.g.add((BODS.declarationIdString, RDFS.range, RDFS.Literal))
        self.g.add((BODS.declarationIdString, RDFS.label, Literal(self.get_title("/$defs/Statement/properties/declaration"))))
        self.g.add((BODS.declarationIdString, RDFS.comment, Literal(self.get_description("/$defs/Statement/properties/declaration"))))

        self.g.add((BODS.declarationSubject, RDF.type, RDF.Property))
        self.g.add((BODS.declarationSubject, RDFS.domain, BODS.Declaration))
        self.g.add((BODS.declarationSubject, RDFS.range, BODS.Entity))
        self.g.add((BODS.declarationSubject, RDFS.range, BODS.Person))
        self.g.add((BODS.declarationSubject, RDFS.label, Literal(self.get_title("/$defs/Statement/properties/declarationSubject"))))
        self.g.add((BODS.declarationSubject, RDFS.comment, Literal(self.get_description("/$defs/Statement/properties/declarationSubject"))))

    def map_record(self):
        self.g.add((BODS.RecordDetails, RDF.type, OWL.Class))
        self.g.add((BODS.RecordDetails, RDFS.label, Literal(self.get_title("/$defs/Statement/properties/recordDetails"))))
        self.g.add((BODS.RecordDetails, RDFS.comment, Literal(self.get_description("/$defs/Statement/properties/recordDetails"))))

    def map_entity(self):
        path = "urn:entity"
        self.map_class(BODS.Entity, path)
        self.g.add((BODS.Entity, RDFS.subClassOf, BODS.RecordDetails))

        # Entity properties
        self.map_properties(BODS.Entity, path)
        publiclisting_path = "/$defs/PublicListing"
        self.map_properties(BODS.Entity, publiclisting_path)

        # Flatten entity type properties
        self.g.add((BODS.entitySubtype, RDF.type, RDF.Property))
        self.g.add((BODS.entitySubtype, RDFS.domain, BODS.Entity))
        self.g.add((BODS.entitySubtype, RDFS.label,
          Literal(self.get_title("/properties/entityType/properties/subtype"))))
        self.g.add((BODS.entitySubtype, RDFS.comment,
          Literal(self.get_description("/properties/entityType/properties/subtype"))))
        self.g.add((BODS.entityTypeDetails, RDF.type, RDF.Property))
        self.g.add((BODS.entityTypeDetails, RDFS.domain, BODS.Entity))
        self.g.add((BODS.entityTypeDetails, RDFS.label,
          Literal("Entity Type Details")))
        self.g.add((BODS.entityTypeDetails, RDFS.comment,
          Literal(self.get_description("/properties/entityType/properties/details"))))
        self.g.add((BODS.entityTypeDetails, RDFS.range, RDFS.Literal))

        # Flatten formedByStatute
        self.g.add((BODS.formedByStatuteDate, RDF.type, RDF.Property))
        self.g.add((BODS.formedByStatuteDate, RDFS.domain, BODS.Entity))
        self.g.add((BODS.formedByStatuteDate, RDFS.label,
          Literal("Formed by Statute Date")))
        self.g.add((BODS.formedByStatuteDate, RDFS.comment,
          Literal(self.get_description("/properties/formedByStatute/properties/date"))))
        self.g.add((BODS.formedByStatuteDate, RDFS.range, XSD.dateTime))
        self.g.add((BODS.formedByStatuteName, RDFS.range, RDFS.Literal))

        # Property ranges that aren't dates or literals
        self.g.add((BODS.address, RDFS.range, BODS.Address))
        self.g.add((BODS.name, RDFS.range, BODS.Name))
        self.g.add((BODS.alternateName, RDFS.range, BODS.Name))
        self.g.add((BODS.jurisdiction, RDFS.range, BODS.Jurisdiction))
        self.g.add((BODS.identifier, RDFS.range, BODS.Identifier))
        self.g.add((BODS.securitiesListing, RDFS.range, BODS.SecuritiesListing))
        self.g.add((BODS.entityType, RDFS.range, BODS.EntityType))
        self.g.add((BODS.entitySubtype, RDFS.range, BODS.EntitySubtype))
        self.g.add((BODS.hasPublicListing, RDFS.range, XSD.Boolean))
        self.g.add((BODS.securitiesListing, RDFS.range, BODS.SecuritiesListing))
        self.g.add((BODS.companyFilingsURL, RDFS.range, RDFS.Resource))

        # Entity type and subtype instances
        self.map_instances(BODS.EntityType, "entityType.csv")
        self.map_instances(BODS.EntitySubtype, "entitySubtype.csv")

    def map_person(self):
        path = "urn:person"
        self.map_class(BODS.Person, path)
        self.g.add((BODS.Person, RDFS.subClassOf, BODS.RecordDetails))

        # Person properties
        self.map_properties(BODS.Person, path)

        # Property ranges that aren't automatically filled
        self.g.add((BODS.personType, RDFS.range, BODS.PersonType))
        self.g.add((BODS.identifier, RDFS.range, BODS.Identifier))
        self.g.add((BODS.name, RDFS.range, BODS.Name))
        self.g.add((BODS.nationality, RDFS.range, BODS.Jurisdiction))
        self.g.add((BODS.placeOfBirth, RDFS.range, BODS.Address))
        self.g.add((BODS.address, RDFS.range, BODS.Address))
        self.g.add((BODS.taxResidency, RDFS.range, BODS.Jurisdiction))
        self.g.add((BODS.politicalExposure, RDFS.range, BODS.PoliticalExposure))
        self.g.remove((BODS.personType, RDFS.range, RDFS.Literal))

        # Flatten politicalExposure/status -> PEPStatus
        pepstatus_path = "/properties/politicalExposure/properties/status"
        self.g.add((BODS.pepStatus, RDF.type, RDF.Property))
        self.g.add((BODS.pepStatus, RDFS.domain, BODS.Person))
        self.g.add((BODS.pepStatus, RDFS.label,
          Literal(self.get_title(pepstatus_path))))
        self.g.add((BODS.pepStatus, RDFS.comment,
          Literal(self.get_description(pepstatus_path))))
        self.g.add((BODS.pepStatus, RDFS.range, BODS.PEPStatus))

        # Person types
        self.map_instances(BODS.PersonType, "personType.csv")

    def map_relationship(self):
        path = "urn:relationship"
        self.map_class(BODS.Relationship, path)
        self.g.add((BODS.Relationship, RDFS.subClassOf, BODS.RecordDetails))

        # Relationship properties
        self.map_properties(BODS.Relationship, path)

        # Property ranges not autofilled (all of them in this case)
        self.g.add((BODS.subject, RDFS.range, BODS.Entity))
        self.g.add((BODS.interestedParty, RDFS.range, BODS.Entity))
        self.g.add((BODS.interestedParty, RDFS.range, BODS.Person))
        self.g.add((BODS.interest, RDFS.range, BODS.Interest))

    def map_unspecified(self):
        path = "/$defs/UnspecifiedRecord"
        self.map_class(BODS.Unspecified, path)
        self.g.add((BODS.Unspecified, RDFS.subClassOf, BODS.RecordDetails))

        # Unspecified Record properties
        self.map_properties(BODS.Unspecified, path)

        # Range fixup
        self.g.add((BODS.unspecifiedReason, RDFS.range, BODS.UnspecifiedReason))
        self.g.remove((BODS.unspecifiedReason, RDFS.range, RDFS.Literal))

        # Unspecified Reason codelist
        self.map_instances(BODS.UnspecifiedReason, "unspecifiedReason.csv")

    def map_interest(self):
        path = "/$defs/Interest"
        self.map_class(BODS.Interest, path)

        # Interest types
        self.map_types(BODS.Interest, BODS.InterestType, "interestType.csv")

        # Interest properties
        self.map_properties(BODS.Interest, path)
        ## flatten share
        share_path = f"{path}/properties/share"
        self.map_properties(BODS.Interest, share_path)
        
        # Ranges
        self.g.add((BODS.beneficialOwnershipOrControl, RDFS.range, XSD.boolean))
        self.g.add((BODS.shareMaximum, RDFS.range, XSD.float))
        self.g.add((BODS.shareMinimum, RDFS.range, XSD.float))
        self.g.add((BODS.shareExact, RDFS.range, XSD.float))
        self.g.add((BODS.shareExclusiveMaximum, RDFS.range, XSD.float))
        self.g.add((BODS.shareExclusiveMinimum, RDFS.range, XSD.float))

    def map_address(self):
        path = "/$defs/Address"
        self.map_class(BODS.Address, path)

        # Address types
        self.map_types(BODS.Address, BODS.AddressType, "addressType.csv")

        # Address properties
        self.map_properties(BODS.Address, path)
        self.g.add((BODS.country, RDFS.range, BODS.Jurisdiction))

    def map_agent(self):
        """
        Agent is a new class for the RDF vocab, not present in the JSON schema.
        """
        self.g.add((BODS.Agent, RDF.type, OWL.Class))
        self.g.add((BODS.agentName, RDF.type, RDF.Property))
        self.g.add((BODS.agentName, RDFS.domain, BODS.Agent))
        self.g.add((BODS.agentName, RDFS.range, RDFS.Literal))
        self.g.add((BODS.agentName, RDFS.label, Literal("Agent name")))
        self.g.add((BODS.agentName, RDFS.comment,
          Literal("The name of the agent responsible for this action")))
        self.g.add((BODS.agentUri, RDF.type, RDF.Property))
        self.g.add((BODS.agentUri, RDFS.domain, BODS.Agent))
        self.g.add((BODS.agentUri, RDFS.range, RDFS.Resource))
        self.g.add((BODS.agentUri, RDFS.label, Literal("Agent URI")))
        self.g.add((BODS.agentUri, RDFS.comment,
          Literal("A globally unique identifier or URL for this agent")))

    def map_annotation(self):
        path = "/$defs/Annotation"
        self.map_class(BODS.Annotation, path)
        self.map_instances(BODS.AnnotationMotivation,
          "annotationMotivation.csv")

        # Properties
        self.map_properties(BODS.Annotation, path)

        # Range fixup
        self.g.add((BODS.motivation, RDFS.range, BODS.AnnotationMotivation))
        self.g.remove((BODS.motivation, RDFS.range, RDFS.Literal))
        self.g.add((BODS.createdBy, RDFS.range, BODS.Agent))

        # TODO duplicate property description

    def map_jurisdiction(self):
        path = "/$defs/Jurisdiction"
        self.map_class(BODS.Jurisdiction, path)

        # Jurisdiction properties
        self.map_properties(BODS.Jurisdiction, path)
        # TODO: name needs converting to jurisdictionName

    def map_identifier(self):
        path = "/$defs/Identifier"
        self.map_class(BODS.Identifier, path)

        # Identifier properties
        self.map_properties(BODS.Identifier, path)

    def map_name(self):
        path = "/$defs/Name"
        self.map_class(BODS.Name, path)

        # Name types
        self.map_types(BODS.Name, BODS.NameType, "nameType.csv")

        # Name properties
        self.map_properties(BODS.Name, path)

    def map_pepstatus(self):
        path = "/properties/politicalExposure/properties/status"
        self.map_class(BODS.PEPStatus, path)

        self.g.add((BODS.NotPEP, RDF.type, BODS.PEPStatus))
        self.g.add((BODS.PEP, RDF.type, BODS.PEPStatus))
        self.g.add((BODS.PEPMissing, RDF.type, BODS.PEPStatus))

    def map_politicalexposure(self):
        path = "/$defs/PepStatusDetails"
        self.map_class(BODS.PoliticalExposure, path)
        self.map_properties(BODS.PoliticalExposure, path)

        self.g.add((BODS.source, RDFS.range, BODS.Source))
        self.g.add((BODS.jurisdiction, RDFS.range, BODS.Jurisdiction))

        # TODO reason and jurisdiction are duplicate properties


    def map_securitieslisting(self):
        pass

    def map_securitiesidentifier(self):
        pass

    def map_source(self):
        pass


    def get_title(self, pointer):
        path = f"{pointer}/title"
        try:
            bit = find_a_bit(self.registry, path)
            return bit.contents
        except:
            return

    def get_description(self, pointer):
        path = f"{pointer}/description"
        try:
            bit = find_a_bit(self.registry, path)
            return bit.contents
        except:
            return

    def rename_property(self, prop):
        if prop in self.rename:
            try:
                return self.rename_map[prop]
            except KeyError:
                # Make single from plural - just remove the s
                return prop[:-1]
        return prop

    def get_property_range(self, path, prop):
        try:
            t = get_type(self.registry, path)
            if t == "string":
                if prop in self.date_props:
                    return XSD.dateTime
                elif prop in self.uri_props:
                    return RDFS.Resource
                elif prop in self.name_props:
                    return BODS.Name
                else:
                    return RDFS.Literal
        except AttributeError:
            pass

    def ttl(self):
        return self.g.serialize(format="turtle", auto_compact=True)

    def write_ttl(self):
        with open("bods-vocabulary-0.4.0.ttl", "w") as f:
            f.write(self.ttl())

    def write_docs(self, filename="bodsvocab.html"):
        od = OntPub(ontology=self.ttl())
        html = od.make_html(destination=filename)


if __name__ == "__main__":

    schemas, codelists = get_schemas_and_codelists()

    vocab = BODSVocab(schemas, codelists)
    vocab.metadata("https://standard.openownership.org/terms",
      "Beneficial Ownership Data Standard v0.4",
      "The RDF vocabulary for the Beneficial Ownership Data Standard v0.4")
    
    # Properties that aren't making it to the RDF model
    vocab.exclude_properties(["statementId", "publicationDetails",
      "declarationSubject", "declaration", "recordId", "recordType",
      "recordStatus", "isComponent", "type", "unspecifiedEntityDetails",
      "publicListing", "unspecifiedPersonDetails", "componentRecords", "share"])
    
    # Properties that need to be renamed (usually from singular to plural)
    rename_map = {
        "addresses": "address",
        "formedByStatute": "formedByStatuteName",
        "nationalities": "nationality",
        "taxResidencies": "taxResidency",
        "reason": "unspecifiedReason",
        "description": "unspecifiedDescription",
        "minimum": "shareMinimum",
        "maximum": "shareMaximum",
        "exact": "shareExact",
        "exclusiveMinimum": "shareExclusiveMinimum",
        "exclusiveMaximum": "shareExclusiveMaximum",
        "address": "streetAddress",
        "id": "idString"
    }
    vocab.rename_properties(["annotations", "alternateNames",
      "identifiers", "names", "securitiesListings", "companyFilingsURLs", "interests"] + list(rename_map.keys()), rename_map)

    # Properties that will have a special type in the RDF model
    vocab.property_ranges(
      date_props=["statementDate", "publicationDate",
      "dissolutionDate", "formedByStatuteDate", "foundingDate", "birthDate",
      "deathDate", "startDate", "endDate"],
      uri_props=["uri", "companyFilingsURL"],
      name_props=["name", "alternateName"]
    )
    
    vocab.make_graph()
    # print(vocab.ttl())
    vocab.write_ttl()
    vocab.write_docs()




