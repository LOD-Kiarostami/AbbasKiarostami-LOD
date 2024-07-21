import xml.etree.ElementTree as ET
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS, OWL

# Parsing the XML file
try:
    tree = ET.parse('a-wolf-lying-in-wait.xml')
    root = tree.getroot()
except ET.ParseError as e:
    print(f"Error parsing XML: {e}")
    raise

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
DBO = Namespace("http://dbpedia.org/ontology/")
SCHEMA = Namespace("https://schema.org")
EX = Namespace('https://w3id.org/AbbasKiarostami-LOD/')

# Extracting XML nodes with checks for None
title = root.find(".//tei:bibl/tei:title", NS)
author_forename = root.find(".//tei:bibl/tei:author/tei:persName/tei:forename", NS)
author_surname = root.find(".//tei:bibl/tei:author/tei:persName/tei:surname", NS)
editors = root.findall(".//tei:bibl/tei:editor", NS)
publisher = root.find(".//tei:bibl/tei:publisher", NS)
date = root.find(".//tei:bibl/tei:date", NS)
ISBN = root.find(".//tei:bibl/tei:idno[@type='ISBN']", NS)
location = root.find(".//tei:bibl/tei:pubPlace/tei:placeName", NS)
geo = root.find(".//tei:bibl/tei:pubPlace/tei:idno[@type='GeoNames']", NS)
dp_teh=root.find(".//tei:pubPlace/tei:idno[@type='DBpedia']",NS)
id_Kiarostami = root.find(".//tei:bibl/tei:author/tei:idno[@type='VIAF']", NS)
birth=root.find(".//tei:author/tei:birth[@when]",NS)
death=root.find(".//tei:death[@when]",NS)
source_url = root.find(".//tei:bibl/tei:ptr[@target]", NS)


# Initialize RDF graph
g = Graph()
g.bind("kiarostami", EX)
g.bind("SCHEMA", SCHEMA)
g.bind("DCTERMS", DCTERMS)
g.bind("OWL",OWL)


# Create a subject for the bibl entry
bibl_subject = URIRef(EX + '/item/'+(title.text.replace(' ', '-') if title is not None else 'unknown-title'))
loc_subject = URIRef(EX + '/place/' + (location.text if location is not None else 'unknown-location'))
auth_subject = URIRef(EX + '/person/' + (f"{author_forename.text}-{author_surname.text}".replace(' ', '-') if author_forename is not None and author_surname is not None else 'unknown-author'))

def add_triple(subject, predicate, obj):
    if obj is not None:
        g.add((subject, predicate, obj))

# Add triples with null checks
add_triple(bibl_subject, DCTERMS.title, Literal(title.text if title is not None else 'No Title'))
add_triple(bibl_subject, DCTERMS.creator, Literal(f"{author_forename.text} {author_surname.text}".strip() if author_forename is not None and author_surname is not None else 'No Author'))
add_triple(bibl_subject, SCHEMA.datePublished, Literal(date.text if date is not None else 'No Date'))
add_triple(bibl_subject, DCTERMS.publisher, Literal(publisher.text if publisher is not None else 'No Publisher'))
add_triple(bibl_subject, DCTERMS.identifier, Literal(ISBN.text if ISBN is not None else 'No ISBN'))
add_triple(auth_subject, OWL.sameAs, URIRef(id_Kiarostami.text if id_Kiarostami is not None else ''))
add_triple(auth_subject, SCHEMA.birthDate, Literal(birth.text if birth is not None else ''))
add_triple(auth_subject, SCHEMA.deathDate, Literal(death.text if death is not None else ''))
add_triple(loc_subject, OWL.sameAs, URIRef(geo.text if geo is not None else ''))
add_triple(loc_subject, OWL.sameAs, URIRef(dp_teh.text if dp_teh is not None else ''))

if source_url is not None:
    add_triple(bibl_subject, SCHEMA.url, URIRef(source_url.attrib['target']))

# Extracting and adding RDF triples
for div in root.findall(".//tei:text/tei:body/tei:div", NS):
    poem_number = div.attrib.get('n', 'unknown-number')
    language = div.attrib.get('lang', 'unknown')
    
    lg = div.find("tei:lg", NS)
    poem_type = lg.attrib.get('type', 'unknown') if lg is not None else 'unknown'
    
    poem_subject = URIRef(EX + 'poem/' + poem_number)
    add_triple(poem_subject, DCTERMS.language, Literal(language))
    add_triple(poem_subject, SCHEMA.genre, Literal(poem_type))
    
    for l in lg.findall("tei:l", NS) if lg is not None else []:
        add_triple(poem_subject, SCHEMA.text, Literal(l.text))



for editor in editors:
    editor_name = editor.find("tei:persName", NS)
    add_triple(bibl_subject, SCHEMA.editor, Literal(editor_name.text if editor_name is not None else editor.text if editor is not None else ''))

# Serialize to Turtle format
turtle = g.serialize(format="turtle", base=EX, encoding="utf-8")
with open("TEI-to-RDF-turtle2.ttl", "wb") as f:
    f.write(turtle)
