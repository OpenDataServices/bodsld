import os
import csv
import requests
import logging

from referencing import Registry, Resource, exceptions
from referencing.jsonschema import DRAFT202012
from rdflib.namespace import Namespace, RDF, RDFS, XSD, OWL, DCTERMS
from pylode.profiles.ontpub import OntPub


logging.getLogger("urllib3").setLevel(logging.WARNING)


REMOTE_SCHEMA_DIR = "https://raw.githubusercontent.com/openownership/data-standard/refs/heads/main/schema/"
SCHEMA_FILES = [
  "components.json",
  "entity-record.json",
  "person-record.json",
  "relationship-record.json",
  "statement.json"
]
CODELIST_FILES = [
  "addressType.csv",
  "annotationMotivation.csv",
  "directOrIndirect.csv",
  "entitySubtype.csv",
  "entityType.csv",
  "interestType.csv",
  "nameType.csv",
  "personType.csv",
  "recordStatus.csv",
  "recordType.csv",
  "securitiesIdentifierSchemas.csv",
  "sourceType.csv",
  "unspecifiedReason.csv"
]


def cap_first(s):
    return s[:1].upper() + s[1:]


def get_remote_schemas():
    schema_files = []
    for fn in SCHEMA_FILES:
        r = requests.get(os.path.join(REMOTE_SCHEMA_DIR, fn))
        j = r.json()
        schema_files.append(j)
    return schema_files


def get_remote_codelists():
    codelist_files = {}
    for fn in CODELIST_FILES:
        r = requests.get(os.path.join(REMOTE_SCHEMA_DIR, "codelists", fn))
        t = r.text
        codelist_files[fn] = t
    return codelist_files


def get_codes(codelist_files, filename):
    codes = []
    cl = codelist_files.get(filename)
    csvfile = cl.split("\n")
    reader = csv.DictReader(csvfile)
    for row in reader:
        codes.append(row.get('code'))
    return codes


def get_codes_and_info(codelist_files, filename):
    codes = {}
    cl = codelist_files.get(filename)
    csvfile = cl.split("\n")
    reader = csv.DictReader(csvfile)
    for row in reader:
        codes[row.get('code')] = (row.get('title'), row.get('description'))
    return codes


def find_a_bit(registry, pointer):
    # looks through all the schemas to resolve the pointer
    # not smart enough to search subresources, so needs a full json pointer
    if "urn:" in pointer:
        # Get the root
        schema = registry.get_or_retrieve(pointer)
        return schema.value.pointer("", registry.resolver())
    else:
        for urn in registry:
            schema = registry.get_or_retrieve(urn)
            try:
                return schema.value.pointer(pointer, registry.resolver())
            except exceptions.PointerToNowhere:
                pass


def get_properties(registry, pointer):
    r = find_a_bit(registry, pointer)
    try:
        return [*r.contents.get("properties")]
    except AttributeError:
        return





def get_type(registry, pointer):
    path = f"{pointer}/type"
    bit = find_a_bit(registry, path)
    return bit.contents





def schema_registry(schema_files):
    schemas = []
    for schema in schema_files:
        schemas.append((schema.get("$id"),
            Resource(contents=schema, specification=DRAFT202012)))

    registry = Registry().with_resources(schemas)
    return registry


def schema_resources(schema_files):
    schemas = []
    for schema in schema_files:
        schemas.append(Resource(contents=schema, specification=DRAFT202012))
    return schemas
