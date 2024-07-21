import csv
import rdflib
from rdflib import Namespace, URIRef, Literal, Graph
from rdflib.namespace import RDF, OWL, RDFS, DCTERMS
import re

#The base URI and namespace mappings
BASE = Namespace("https://w3id.org/AbbasKiarostami-LOD/")
namespace_mappings = {
    "SCHEMA": Namespace("https://schema.org/"),
    "DBO": Namespace("http://dbpedia.org/ontology/"),
    "CRM": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "RDF": RDF,
    "RDFS":RDFS,
    "OWL": OWL,
    "DCTERMS": DCTERMS,
    "XSD": Namespace("http://www.w3.org/2001/XMLSchema#"),
    "TIME": Namespace("http://www.w3.org/2006/time#"),
    "FRBROO": Namespace("http://iflastandards.info/ns/fr/frbroo/"),  # Example for FRBROO namespace
}

# Create a new RDF graph
g = Graph()

# Bind namespaces to prefixes
for prefix, namespace in namespace_mappings.items():
    g.bind(prefix.lower(), namespace)

# Function to resolve prefixed properties to full URIRefs
def resolve_prefixed_property(prefixed_property):
    try:
        if ':' in prefixed_property:
            namespace, local_name = prefixed_property.split(":", 1)
            namespace = namespace_mappings[namespace.upper()]
            return namespace[local_name.strip()]
        else:
            raise ValueError("Invalid prefixed property format")
    except Exception as e:
        print(f"Error resolving prefixed property '{prefixed_property}': {e}")
        return None

# Function to convert a value to URIRef or Literal
def convert_value(value):
    value = value.strip()
    if value.startswith("http://") or value.startswith("https://"):
        return URIRef(value)
    else:
        return Literal(value)

# Function to create a local URI from the BASE and SUBJECT
def create_local_uri(subject):
    sanitized_subject = subject.replace(' ', '-')
    return URIRef(BASE + sanitized_subject)

# Function to match internal URIs
def matches_internal_uri(input_string):
    pattern = r"[a-z]+:\w+"
    return bool(re.match(pattern, input_string))

# Function to match dates
def matches_dates(input_string):
    pattern = r"\d{4}(\/\d{2}(\/\d{1,2})?)?"
    return bool(re.match(pattern, input_string))

# CSV files
csv_files = [
    'certifiedCopy.csv',
    'poster.csv',
    'event.csv',
    'poem.csv',
    'sig.csv',
    'doc.csv',
    'portrait.csv',
    'photo.csv',
    'imageMaker.csv',
    'book.csv',
    'abbasKiarostami.csv',
    'otherRelations.csv'
]

# Root directory for CSV files
root = '../csv-files/'

# Internal URI types
internal_uri_types = [
    "person/",
    "item/",
    "place/",
    "date/",
    "event/",
    "language/",
    "organization/",
    "award/",
    "object",
    "movie"
]

# Read and process each CSV file
for csv_f in csv_files:
    with open(root + csv_f, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Create subject URI
            s = create_local_uri(row['SUBJECT'])
            
            # Resolve predicate to full URI
            p = resolve_prefixed_property(row['PREDICATE'])
            if p is None:
                continue
            
            # Determine object type and convert
            o = row['OBJECT'].strip()
            if any(uri_type in o for uri_type in internal_uri_types):
                o = create_local_uri(o)
            elif matches_internal_uri(o):
                o = resolve_prefixed_property(o)
                if o is None:
                    continue
            elif "http://" in o or "https://" in o:
                o = URIRef(o)
            elif matches_dates(o):
                o = Literal(o, datatype=namespace_mappings["SCHEMA"].Date)
            else:
                o = Literal(o)
            
            # Add triple to the graph
            g.add((s, p, o))


# Serialize the graph to a Turtle file
turtle_str = g.serialize(format="turtle", base=BASE, encoding="utf-8")
with open("rdf-production.ttl", "wb") as f:
    f.write(turtle_str)
