import re
import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS
from slugify import slugify


CSV_PATH  = "data/tautiba.csv"
TAUT_PATH = "data/TAUT2016_11012026_015802.csv"
ATVK_PATH = "data/ATVK2021_11012026_015924.csv"
OUT_TTL   = "tautiba_datacube.ttl"

-
COL_AREA = "AllAreaLV"
COL_TIME = "TIME"
COL_ETH  = "ETHNICITY"

MEASURE_NUMB = "NUMB"   
MEASURE_PC   = "PC"       
ATTR_NUMB_X  = "NUMB_X"   
ATTR_PC_X    = "PC_X"     

QB   = Namespace("http://purl.org/linked-data/cube#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
EX   = Namespace("https://NiklavsPS.github.io/tautiba-rdf-datacube/")  
YEAR = Namespace("http://reference.data.gov.uk/id/gregorian-year/")

g = Graph()
g.bind("qb", QB)
g.bind("skos", SKOS)
g.bind("ex", EX)
g.bind("rdfs", RDFS)
g.bind("dcterms", DCTERMS)

def slug(v: str) -> str:
    return slugify(str(v), lowercase=True)

def extract_digits(s: str):
    nums = re.findall(r"\d+", str(s))
    return int("".join(nums)) if nums else None

def to_int_or_none(x: str):
    try:
        return int(str(x).strip())
    except:
        return None


taut_df = pd.read_csv(TAUT_PATH, dtype=str).fillna("")
atvk_df = pd.read_csv(ATVK_PATH, dtype=str).fillna("")

taut_map_code_to_name = {}
for _, r in taut_df.iterrows():
    kods = to_int_or_none(r.get("Kods", ""))
    nos = str(r.get("Nosaukums", "")).strip()
    if kods is not None and nos:
        taut_map_code_to_name[kods] = nos

atvk_map_code_to_name = {}
for _, r in atvk_df.iterrows():
    kods = to_int_or_none(r.get("Kods", ""))
    nos = str(r.get("Nosaukums", "")).strip()
    if kods is not None and nos:
        atvk_map_code_to_name[kods] = nos

# Pievienoju atbilstoši klasifikatoram lai taut klasifikators nedaudz savienotos
eth_to_taut = {
    "E_LAT": 1,
    "E_LIT": 2,
    "E_EST": 3,
    "E_AZE": 12,
    "E_BRU": 13,
    "E_GEO": 14,
    "E_ARM": 15,
    "E_RUS": 17,
    "E_MOL": 18,
    "E_UKR": 21,
    "E_UZB": 22,
    "E_POL": 45,
    "E_JEW": 68,
    "E_TTR": 242,
    "E_ROM": 313,
    "E_IND": 295,
}

dataset = EX["dataset/tautiba"]
dsd = EX["dsd/tautiba"]

dim_area = EX["dim/refArea"]
dim_time = EX["dim/refPeriod"]
dim_eth  = EX["dim/ethnicity"]

m_numb = EX["measure/numb"]
m_pc   = EX["measure/pc"]

a_numb_x = EX["attr/numb_x"]
a_pc_x   = EX["attr/pc_x"]

# pieejamie publiskie metadati
g.add((dataset, RDF.type, QB.DataSet))
g.add((dataset, RDFS.label, Literal("Iedzīvotāju skaits pēc tautības (RDF Data Cube)", lang="lv")))
g.add((dataset, DCTERMS.title, Literal("Population by ethnicity (RDF Data Cube)", lang="en")))
g.add((dataset, QB.structure, dsd))

g.add((dsd, RDF.type, QB.DataStructureDefinition))

def add_component_dimension(dimension_uri):
    cs = URIRef(str(dsd) + "/component/" + slug(str(dimension_uri).split("/")[-1]))
    g.add((dsd, QB.component, cs))
    g.add((cs, QB.dimension, dimension_uri))

def add_component_measure(measure_uri):
    cs = URIRef(str(dsd) + "/component/" + slug(str(measure_uri).split("/")[-1]))
    g.add((dsd, QB.component, cs))
    g.add((cs, QB.measure, measure_uri))

def add_component_attribute(attr_uri):
    cs = URIRef(str(dsd) + "/component/" + slug(str(attr_uri).split("/")[-1]))
    g.add((dsd, QB.component, cs))
    g.add((cs, QB.attribute, attr_uri))

add_component_dimension(dim_area)
add_component_dimension(dim_time)
add_component_dimension(dim_eth)
add_component_measure(m_numb)
add_component_measure(m_pc)
add_component_attribute(a_numb_x)
add_component_attribute(a_pc_x)


g.add((dim_area, RDF.type, QB.DimensionProperty))
g.add((dim_area, RDFS.label, Literal("Teritorija", lang="lv")))

g.add((dim_time, RDF.type, QB.DimensionProperty))
g.add((dim_time, RDFS.label, Literal("Gads", lang="lv")))

g.add((dim_eth, RDF.type, QB.DimensionProperty))
g.add((dim_eth, RDFS.label, Literal("Tautība", lang="lv")))


g.add((m_numb, RDF.type, QB.MeasureProperty))
g.add((m_numb, RDFS.label, Literal("Skaits", lang="lv")))
g.add((m_numb, RDFS.label, Literal("Number", lang="en")))

g.add((m_pc, RDF.type, QB.MeasureProperty))
g.add((m_pc, RDFS.label, Literal("%", lang="lv")))
g.add((m_pc, RDFS.label, Literal("per cent", lang="en")))

g.add((a_numb_x, RDF.type, QB.AttributeProperty))
g.add((a_numb_x, RDFS.label, Literal("NUMB papildu/atzīmes", lang="lv")))

g.add((a_pc_x, RDF.type, QB.AttributeProperty))
g.add((a_pc_x, RDFS.label, Literal("PC papildu/atzīmes", lang="lv")))


scheme_area = EX["codelist/area"]
scheme_eth  = EX["codelist/ethnicity"]

g.add((scheme_area, RDF.type, SKOS.ConceptScheme))
g.add((scheme_area, RDFS.label, Literal("Teritoriju kodu saraksts (AllAreaLV)", lang="lv")))

g.add((scheme_eth, RDF.type, SKOS.ConceptScheme))
g.add((scheme_eth, RDFS.label, Literal("Tautību kodu saraksts (ETHNICITY)", lang="lv")))

g.add((dim_area, QB.codeList, scheme_area))
g.add((dim_eth, QB.codeList, scheme_eth))


scheme_atvk_official = EX["classifier/atvk2021"]
scheme_taut_official = EX["classifier/taut2016"]

g.add((scheme_atvk_official, RDF.type, SKOS.ConceptScheme))
g.add((scheme_atvk_official, RDFS.label, Literal("ATVK 2021 (klasifikators)", lang="lv")))

g.add((scheme_taut_official, RDF.type, SKOS.ConceptScheme))
g.add((scheme_taut_official, RDFS.label, Literal("TAUT 2016 (klasifikators)", lang="lv")))


df = pd.read_csv(CSV_PATH, sep=";")


for col in [MEASURE_NUMB, MEASURE_PC, ATTR_NUMB_X, ATTR_PC_X, COL_TIME]:
    df[col] = pd.to_numeric(df[col], errors="coerce")


for idx, row in df.iterrows():
    area_code = row.get(COL_AREA)
    eth_code  = row.get(COL_ETH)
    year_val  = row.get(COL_TIME)

    if pd.isna(year_val) or pd.isna(area_code) or pd.isna(eth_code):
        continue

    year_uri = YEAR[str(int(year_val))]


    area_uri = EX[f"concept/area/{slug(area_code)}"]
    g.add((area_uri, RDF.type, SKOS.Concept))
    g.add((area_uri, SKOS.inScheme, scheme_area))
    g.add((area_uri, SKOS.notation, Literal(str(area_code))))

    area_digits = extract_digits(area_code)
    if area_digits and area_digits in atvk_map_code_to_name:
        g.add((area_uri, SKOS.prefLabel, Literal(atvk_map_code_to_name[area_digits], lang="lv")))

        atvk_uri = EX[f"concept/atvk2021/{area_digits}"]
        g.add((atvk_uri, RDF.type, SKOS.Concept))
        g.add((atvk_uri, SKOS.inScheme, scheme_atvk_official))
        g.add((atvk_uri, SKOS.notation, Literal(str(area_digits))))
        g.add((atvk_uri, SKOS.prefLabel, Literal(atvk_map_code_to_name[area_digits], lang="lv")))

        g.add((area_uri, SKOS.exactMatch, atvk_uri))
    else:
        g.add((area_uri, SKOS.prefLabel, Literal(str(area_code))))


    eth_uri = EX[f"concept/ethnicity/{slug(eth_code)}"]
    g.add((eth_uri, RDF.type, SKOS.Concept))
    g.add((eth_uri, SKOS.inScheme, scheme_eth))
    g.add((eth_uri, SKOS.notation, Literal(str(eth_code))))

    taut_code = eth_to_taut.get(str(eth_code))
    if taut_code and taut_code in taut_map_code_to_name:
        g.add((eth_uri, SKOS.prefLabel, Literal(taut_map_code_to_name[taut_code], lang="lv")))

        taut_uri = EX[f"concept/taut2016/{taut_code}"]
        g.add((taut_uri, RDF.type, SKOS.Concept))
        g.add((taut_uri, SKOS.inScheme, scheme_taut_official))
        g.add((taut_uri, SKOS.notation, Literal(str(taut_code))))
        g.add((taut_uri, SKOS.prefLabel, Literal(taut_map_code_to_name[taut_code], lang="lv")))

        g.add((eth_uri, SKOS.exactMatch, taut_uri))
    else:
        g.add((eth_uri, SKOS.prefLabel, Literal(str(eth_code))))


    obs = EX[f"obs/{idx}"]
    g.add((obs, RDF.type, QB.Observation))
    g.add((obs, QB.dataSet, dataset))

    g.add((obs, dim_area, area_uri))
    g.add((obs, dim_time, year_uri))
    g.add((obs, dim_eth, eth_uri))

    numb = row.get(MEASURE_NUMB)
    pc   = row.get(MEASURE_PC)
    if not pd.isna(numb):
        g.add((obs, m_numb, Literal(int(numb), datatype=XSD.integer)))
    if not pd.isna(pc):
        g.add((obs, m_pc, Literal(float(pc), datatype=XSD.decimal)))

    numb_x = row.get(ATTR_NUMB_X)
    pc_x   = row.get(ATTR_PC_X)
    if not pd.isna(numb_x):
        g.add((obs, a_numb_x, Literal(int(numb_x), datatype=XSD.integer)))
    if not pd.isna(pc_x):
        g.add((obs, a_pc_x, Literal(int(pc_x), datatype=XSD.integer)))

g.serialize(destination=OUT_TTL, format="turtle")
print(f"OK: saved {OUT_TTL} | triples: {len(g)}")
