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

    def map_properties(self, path, domain):
        properties = get_properties(self.registry, path)
        props = {}
        for p in properties:
            if p not in self.exclude:
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

    def make_graph(self):
        # self.map_statement()
        # self.map_declaration()
        # self.map_record()
        # self.map_person()
        # self.map_person_types()
        # self.map_entity()
        # self.map_entity_types()
        # self.map_relationship()
        # self.map_unspecified()
        # self.map_interest()
        # self.map_interest_types()
        self.map_address()

    def map_statement(self):
        self.g.add((BODS.Statement, RDF.type, OWL.Class))
        self.g.add((BODS.Statement, RDFS.label,
            Literal(self.get_title("/$defs/Statement"))))
        self.g.add((BODS.Statement, RDFS.comment,
            Literal(self.get_description("/$defs/Statement"))))

        # Turn recordStatus codelist into classes

        record_status = get_codes_and_info(self.codelists, "recordStatus.csv")

        self.g.add((BODS.NewRecordStatement, RDF.type, OWL.Class))
        self.g.add((BODS.NewRecordStatement, RDFS.subClassOf, BODS.Statement))
        self.g.add((BODS.NewRecordStatement, RDFS.label, Literal(record_status.get('new')[0])))
        self.g.add((BODS.NewRecordStatement, RDFS.comment, Literal(record_status.get('new')[1])))
        self.g.add((BODS.UpdatedRecordStatement, RDF.type, OWL.Class))
        self.g.add((BODS.UpdatedRecordStatement, RDFS.subClassOf, BODS.Statement))
        self.g.add((BODS.UpdatedRecordStatement, RDFS.label, Literal(record_status.get('updated')[0])))
        self.g.add((BODS.UpdatedRecordStatement, RDFS.comment, Literal(record_status.get('updated')[1])))
        self.g.add((BODS.ClosedRecordStatement, RDF.type, OWL.Class))
        self.g.add((BODS.ClosedRecordStatement, RDFS.subClassOf, BODS.Statement))
        self.g.add((BODS.ClosedRecordStatement, RDFS.label, Literal(record_status.get('closed')[0])))
        self.g.add((BODS.ClosedRecordStatement, RDFS.comment, Literal(record_status.get('closed')[1])))

        # Statement properties

        stmt_properties = get_properties(self.registry, "/$defs/Statement")
        pd_properties = get_properties(self.registry, "/$defs/Statement/properties/publicationDetails")
        props = {}
        for sp in stmt_properties:
          if sp not in self.exclude:
            props[sp] = f"/$defs/Statement/properties/{sp}"
        for pdp in pd_properties:
          if pdp not in self.exclude:
            props[pdp] = f"/$defs/Statement/properties/publicationDetails/properties/{pdp}"

        for prop, path in props.items():

          prop_range = self.get_property_range(path, prop)
          prop = self.rename_property(prop)

          self.g.add((BODS[prop], RDF.type, RDF.Property))
          self.g.add((BODS[prop], RDFS.domain, BODS.Statement))
          self.g.add((BODS[prop], RDFS.label, Literal(self.get_title(path))))
          self.g.add((BODS[prop], RDFS.comment, Literal(self.get_description(path))))

          if prop_range:
            self.g.add((BODS[prop], RDFS.range, prop_range))

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
        self.g.add((BODS.Entity, RDF.type, OWL.Class))
        self.g.add((BODS.Entity, RDFS.subClassOf, BODS.RecordDetails))
        self.g.add((BODS.Entity, RDFS.label,
          Literal(self.record_types.get('entity')[0])))
        self.g.add((BODS.Entity, RDFS.comment,
          Literal(self.record_types.get('entity')[1])))


        # Entity properties
        entity_properties = get_properties(self.registry, "urn:entity")
        pl_properties = get_properties(self.registry, "/$defs/PublicListing")
        props = {}
        for ep in entity_properties:
          if ep not in self.exclude:
            props[ep] = f"/properties/{ep}"
        for plp in pl_properties:
          if plp not in self.exclude:
            props[plp] = f"/$defs/PublicListing/properties/{plp}"

        for prop, path in props.items():

          prop_range = self.get_property_range(path, prop)
          prop = self.rename_property(prop)

          title = self.get_title(path) or prop
          description = self.get_description(path) or prop
          self.g.add((BODS[prop], RDF.type, RDF.Property))
          self.g.add((BODS[prop], RDFS.domain, BODS.Entity))
          self.g.add((BODS[prop], RDFS.label, Literal(title)))
          self.g.add((BODS[prop], RDFS.comment, Literal(description)))

          if prop_range:
            self.g.add((BODS[prop], RDFS.range, prop_range))

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

    def map_entity_types(self):
        
        self.g.add((BODS.EntityType, RDF.type, OWL.Class))
        entity_types = get_codes_and_info(self.codelists, "entityType.csv")
        
        for code, info in entity_types.items():
          et = cap_first(code)
          self.g.add((BODS[et], RDF.type, BODS.EntityType))
          self.g.add((BODS[et], RDFS.label, Literal(entity_types.get(code)[0])))
          self.g.add((BODS[et], RDFS.comment, Literal(entity_types.get(code)[1])))

        self.g.add((BODS.EntitySubype, RDF.type, OWL.Class))
        entity_subtypes = get_codes_and_info(self.codelists, "entitySubtype.csv")
        
        for code, info in entity_subtypes.items():
          est = cap_first(code)
          self.g.add((BODS[est], RDF.type, BODS.EntitySubtype))
          self.g.add((BODS[est], RDFS.label, Literal(entity_subtypes.get(code)[0])))
          self.g.add((BODS[est], RDFS.comment, Literal(entity_subtypes.get(code)[1])))

    def map_person(self):
        self.g.add((BODS.Person, RDF.type, OWL.Class))
        self.g.add((BODS.Person, RDFS.subClassOf, BODS.RecordDetails))
        self.g.add((BODS.Person, RDFS.label,
          Literal(self.record_types.get('person')[0])))
        self.g.add((BODS.Person, RDFS.comment,
          Literal(self.record_types.get('person')[1])))

        # Person properties
        person_properties = get_properties(self.registry, "urn:person")
        props = {}
        for pp in person_properties:
            if pp not in self.exclude:
                props[pp] = f"/properties/{pp}"

        for prop, path in props.items():
            prop_range = self.get_property_range(path, prop)
            prop = self.rename_property(prop)

            title = self.get_title(path) or prop
            description = self.get_description(path) or prop
            self.g.add((BODS[prop], RDF.type, RDF.Property))
            self.g.add((BODS[prop], RDFS.domain, BODS.Person))
            self.g.add((BODS[prop], RDFS.label, Literal(title)))
            self.g.add((BODS[prop], RDFS.comment, Literal(description)))

            if prop_range and prop != "personType":
                self.g.add((BODS[prop], RDFS.range, prop_range))

        # Property ranges that aren't automatically filled
        self.g.add((BODS.personType, RDFS.range, BODS.PersonType))
        self.g.add((BODS.identifier, RDFS.range, BODS.Identifier))
        self.g.add((BODS.name, RDFS.range, BODS.Name))
        self.g.add((BODS.nationality, RDFS.range, BODS.Jurisdiction))
        self.g.add((BODS.placeOfBirth, RDFS.range, BODS.Address))
        self.g.add((BODS.address, RDFS.range, BODS.Address))
        self.g.add((BODS.taxResidency, RDFS.range, BODS.Jurisdiction))
        self.g.add((BODS.politicalExposure, RDFS.range, BODS.PoliticalExposure))

        # Flatten politicalExposure/status -> PEPStatus
        pepstatus_path = "/properties/politicalExposure/properties/status"
        self.g.add((BODS.pepStatus, RDF.type, RDF.Property))
        self.g.add((BODS.pepStatus, RDFS.domain, BODS.Person))
        self.g.add((BODS.pepStatus, RDFS.label,
          Literal(self.get_title(pepstatus_path))))
        self.g.add((BODS.pepStatus, RDFS.comment,
          Literal(self.get_description(pepstatus_path))))
        self.g.add((BODS.pepStatus, RDFS.range, BODS.PEPStatus))

    def map_person_types(self):

        self.g.add((BODS.PersonType, RDF.type, OWL.Class))
        person_types = get_codes_and_info(self.codelists, "personType.csv")
        
        for code in person_types:
            pt = cap_first(code)
            self.g.add((BODS[pt], RDF.type, BODS.PersonType))
            self.g.add((BODS[pt], RDFS.label,
              Literal(person_types.get(code)[0])))
            self.g.add((BODS[pt], RDFS.comment,
              Literal(person_types.get(code)[1])))

    def map_relationship(self):
        self.g.add((BODS.Relationship, RDF.type, OWL.Class))
        self.g.add((BODS.Relationship, RDFS.subClassOf, BODS.RecordDetails))
        self.g.add((BODS.Relationship, RDFS.label,
          Literal(self.record_types.get('relationship')[0])))
        self.g.add((BODS.Relationship, RDFS.comment,
          Literal(self.record_types.get('relationship')[1])))

        # Relationship properties
        relationship_properties = get_properties(self.registry, "urn:relationship")
        props = {}
        for rp in relationship_properties:
            if rp not in self.exclude:
                props[rp] = f"/properties/{rp}"

        for prop, path in props.items():
            prop_range = self.get_property_range(path, prop)
            prop = self.rename_property(prop)

            title = self.get_title(path) or prop
            description = self.get_description(path) or prop
            self.g.add((BODS[prop], RDF.type, RDF.Property))
            self.g.add((BODS[prop], RDFS.domain, BODS.Relationship))
            self.g.add((BODS[prop], RDFS.label, Literal(title)))
            self.g.add((BODS[prop], RDFS.comment, Literal(description)))

            if prop_range:
                self.g.add((BODS[prop], RDFS.range, prop_range))

        # Property ranges not autofilled (all of them in this case)
        self.g.add((BODS.subject, RDFS.range, BODS.Entity))
        self.g.add((BODS.interestedParty, RDFS.range, BODS.Entity))
        self.g.add((BODS.interestedParty, RDFS.range, BODS.Person))
        self.g.add((BODS.interest, RDFS.range, BODS.Interest))

    def map_unspecified(self):
        uns_path = "/$defs/UnspecifiedRecord"
        self.g.add((BODS.Unspecified, RDF.type, OWL.Class))
        self.g.add((BODS.Unspecified, RDFS.subClassOf, BODS.RecordDetails))
        self.g.add((BODS.Unspecified, RDFS.label,
          Literal(self.get_title(uns_path))))
        self.g.add((BODS.Unspecified, RDFS.comment,
          Literal(self.get_description(uns_path))))

        # Unspecified Record properties
        uns_properties = get_properties(self.registry, uns_path)
        props = {}
        for up in uns_properties:
            if up not in self.exclude:
                props[up] = f"{uns_path}/properties/{up}"

        for prop, path in props.items():
            prop_range = self.get_property_range(path, prop)
            prop = self.rename_property(prop)

            title = self.get_title(path) or prop
            description = self.get_description(path) or prop
            self.g.add((BODS[prop], RDF.type, RDF.Property))
            self.g.add((BODS[prop], RDFS.domain, BODS.Unspecified))
            self.g.add((BODS[prop], RDFS.label, Literal(title)))
            self.g.add((BODS[prop], RDFS.comment, Literal(description)))

            if prop_range and prop != "unspecifiedReason":
                self.g.add((BODS[prop], RDFS.range, prop_range))

        self.g.add((BODS.unspecifiedReason, RDFS.range, BODS.UnspecifiedReason))

        # Unspecified Reason codelist
        self.g.add((BODS.UnspecifiedReason, RDF.type, OWL.Class))
        unspec_reasons = get_codes_and_info(codelists, "unspecifiedReason.csv")
        for code, info in unspec_reasons.items():
          ur = cap_first(code)
          self.g.add((BODS[ur], RDF.type, BODS.UnspecifiedReason))
          self.g.add((BODS[ur], RDFS.label, Literal(unspec_reasons.get(code)[0])))
          self.g.add((BODS[ur], RDFS.comment, Literal(unspec_reasons.get(code)[1])))


    def map_interest(self):
        interest_path = "/$defs/Interest"
        self.g.add((BODS.Interest, RDF.type, OWL.Class))
        self.g.add((BODS.Interest, RDFS.label,
          Literal(self.get_title(interest_path))))
        self.g.add((BODS.Interest, RDFS.comment,
          Literal(self.get_description(interest_path))))

        # Interest properties
        interest_properties = get_properties(self.registry, interest_path)
        props = {}
        for ip in interest_properties:
            if ip not in self.exclude:
                props[ip] = f"{interest_path}/properties/{ip}"

        # Flatten share
        share_path = f"{interest_path}/properties/share"
        share_properties = get_properties(self.registry, share_path)
        for sp in share_properties:
            if sp not in self.exclude:
                props[sp] = f"{share_path}/properties/{sp}"

        for prop, path in props.items():
            prop_range = self.get_property_range(path, prop)
            prop = self.rename_property(prop)

            title = self.get_title(path) or prop
            description = self.get_description(path) or prop
            self.g.add((BODS[prop], RDF.type, RDF.Property))
            self.g.add((BODS[prop], RDFS.domain, BODS.Interest))
            self.g.add((BODS[prop], RDFS.label, Literal(title)))
            self.g.add((BODS[prop], RDFS.comment, Literal(description)))

            if prop_range:
                self.g.add((BODS[prop], RDFS.range, prop_range))

        # Ranges
        self.g.add((BODS.beneficialOwnershipOrControl, RDFS.range, XSD.boolean))
        self.g.add((BODS.shareMaximum, RDFS.range, XSD.float))
        self.g.add((BODS.shareMinimum, RDFS.range, XSD.float))
        self.g.add((BODS.shareExact, RDFS.range, XSD.float))
        self.g.add((BODS.shareExclusiveMaximum, RDFS.range, XSD.float))
        self.g.add((BODS.shareExclusiveMinimum, RDFS.range, XSD.float))

    def map_interest_types(self):

        self.g.add((BODS.InterestType, RDF.type, OWL.Class))
        interest_types = get_codes_and_info(self.codelists, "interestType.csv")
        
        for code in interest_types:
            it = cap_first(code)
            self.g.add((BODS[it], RDF.type, OWL.Class))
            self.g.add((BODS[it], RDFS.subClassOf, BODS.Interest))
            self.g.add((BODS[it], RDFS.label,
              Literal(interest_types.get(code)[0])))
            self.g.add((BODS[it], RDFS.comment,
              Literal(interest_types.get(code)[1])))

    def map_address(self):
        path = "/$defs/Address"
        self.g.add((BODS.Address, RDF.type, OWL.Class))
        self.g.add((BODS.Address, RDFS.label,
          Literal(self.get_title(path))))
        self.g.add((BODS.Address, RDFS.comment,
          Literal(self.get_description(path))))

        # Address types
        self.g.add((BODS.AddressType, RDF.type, OWL.Class))
        address_types = get_codes_and_info(self.codelists, "addressType.csv")
        
        for code in address_types:
            t = cap_first(code)
            self.g.add((BODS[t], RDF.type, OWL.Class))
            self.g.add((BODS[t], RDFS.subClassOf, BODS.Address))
            self.g.add((BODS[t], RDFS.label,
              Literal(address_types.get(code)[0])))
            self.g.add((BODS[t], RDFS.comment,
              Literal(address_types.get(code)[1])))

        # Address properties
        self.map_properties(path, BODS.Address)
        self.g.add((BODS.country, RDFS.range, BODS.Jurisdiction))

    def map_agent(self):
        pass

    def map_annotation(self):
        pass

    def map_jurisdiction(self):
        pass

    def map_identifier(self):
        pass

    def map_name(self):
        pass

    def map_pepstatus(self):
        pass

    def map_politicalexposure(self):
        pass

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
        "address": "streetAddress"
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




