# Iedzīvotāju skaits pēc tautības - Linked Open Data

Šajā lapā publicēta Latvijas Centrālās statistikas pārvaldes (CSP) statistisko datu kopa
**"Iedzīvotāju skaits pēc tautības"**, kas pārveidota un publicēta
**atvērto saistīto datu (Linked Open Data)** formā kursa darba ietvaros.

Datu kopa ir pārveidota no tabulāra CSV formāta uz **[RDF Data Cube Vocabulary (QB)](https://www.w3.org/TR/vocab-data-cube/)** modeli,
izmantojot starptautiski atzītus semantiskā tīmekļa standartus.

---

## Datu saturs

Datu kopa satur statistiskos novērojumus par:
- iedzīvotāju skaitu (`NUMB`)
- iedzīvotāju īpatsvaru procentos (`PC`)

sadalījumā pēc:
- **teritorijas** (administratīvās teritorijas, statistiskās teritorijas, Rīgas apkaimes u.c.)
- **tautības**
- **gada**

Katrs statistiskais novērojums ir modelēts kā atsevišķs RDF objekts (`qb:Observation`).

---

## Izmantotie standarti un vārdnīcas

Datu publicēšanā izmantoti šādi standarti:
- **[RDF Data Cube Vocabulary (QB)](https://www.w3.org/TR/vocab-data-cube/)** — statistisko datu modelēšanai
- **SKOS** — teritoriju un tautību kodu aprakstam
- **DCAT** — datu kopas metadatu aprakstam
- **RDF / Turtle** — datu serializācijas formāts

Teritoriju kodi balstīti uz atvērto datu portālā izmantotajiem CSP teritoriju kodiem,
savukārt administratīvajām teritorijām nodrošināta sasaite ar **ATVK 2021** klasifikatoru.
Tautību kodi daļēji sasaistīti ar **TAUT 2016** klasifikatoru.

---

## Datu piekļuve

### Metadati
Datu kopas metadati (DCAT, Turtle formātā):
- [metadata.ttl](https://github.com/NiklavsPS/tautiba-rdf-datacube/blob/main/metadata.ttl)

### Pilnā RDF Data Cube datu kopa
Pilnā datu kopa, ņemot vērā tās apjomu, publicēta kā GitHub repozitorija relīzes artefakts:
- [Lejupielādēt RDF Data Cube (.ttl)](https://github.com/NiklavsPS/tautiba-rdf-datacube/releases/download/v1.1/tautiba_datacube.ttl)

Datus iespējams lejupielādēt un ielādēt jebkurā RDF triplestore vai apstrādāt ar SPARQL rīkiem lokāli.

---
## Datu piemērs

Piemērs no publicētajiem datiem

```
    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix ns1: <https://niklavsps.github.io/tautiba-rdf-datacube/dim/> .
    @prefix ns2: <https://niklavsps.github.io/tautiba-rdf-datacube/attr/> .
    @prefix ns3: <https://niklavsps.github.io/tautiba-rdf-datacube/measure/> .
    @prefix qb: <http://purl.org/linked-data/cube#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <https://niklavsps.github.io/tautiba-rdf-datacube/obs/469511> a qb:Observation ;
        qb:dataSet <https://niklavsps.github.io/tautiba-rdf-datacube/dataset/tautiba> ;
        ns1:ethnicity <https://niklavsps.github.io/tautiba-rdf-datacube/concept/ethnicity/e_pol> ;
        ns1:refArea <https://niklavsps.github.io/tautiba-rdf-datacube/concept/area/lv009> ;
        ns1:refPeriod <http://reference.data.gov.uk/id/gregorian-year/2011> ;
        ns3:numb 4028 ;
        ns3:pc 2.0 .

    # --- Teritorija no AllAreaLV (nosaukums no teritorijas.csv) ---
    <https://niklavsps.github.io/tautiba-rdf-datacube/concept/area/lv0001000>
    a skos:Concept ;
    skos:inScheme <https://niklavsps.github.io/tautiba-rdf-datacube/codelist/area> ;
    skos:notation "LV0001000" ;
    skos:prefLabel "Rīga"@lv ;
    skos:prefLabel "Riga"@en ;
    skos:exactMatch <https://niklavsps.github.io/tautiba-rdf-datacube/concept/atvk2021/1000> .

    # --- ATVK koncepts (oficiālais klasifikators) ---
    <https://niklavsps.github.io/tautiba-rdf-datacube/concept/atvk2021/1000>
    a skos:Concept ;
    skos:inScheme <https://niklavsps.github.io/tautiba-rdf-datacube/classifier/atvk2021> ;
    skos:notation "1000" ;
    skos:prefLabel "Rīga"@lv .

    # --- Tautība (ETHNICITY) ar sasaisti uz TAUT 2016 ---
    <https://niklavsps.github.io/tautiba-rdf-datacube/concept/ethnicity/e_lat>
    a skos:Concept ;
    skos:inScheme <https://niklavsps.github.io/tautiba-rdf-datacube/codelist/ethnicity> ;
    skos:notation "E_LAT" ;
    skos:prefLabel "Latvieši"@lv ;
    skos:exactMatch <https://niklavsps.github.io/tautiba-rdf-datacube/concept/taut2016/1> .

    # --- TAUT 2016 koncepts (oficiālais klasifikators) ---
    <https://niklavsps.github.io/tautiba-rdf-datacube/concept/taut2016/1>
    a skos:Concept ;
    skos:inScheme <https://niklavsps.github.io/tautiba-rdf-datacube/classifier/taut2016> ;
    skos:notation "1" ;
    skos:prefLabel "Latvieši"@lv .
```

---

## Piemērs (SPARQL vaicājuma ideja)

Pēc datu lejupielādes lietotājs var, piemēram, atlasīt novērojumu skaitu:

```sparql
PREFIX qb: <http://purl.org/linked-data/cube#>

SELECT (COUNT(?o) AS ?obsCount)
WHERE {
  ?o a qb:Observation .
}
```
---

## Piezīme par URI dereferencējamību

Šajā publicēšanas risinājumā pilnā datu kopa ir pieejama kā RDF “bulk download” fails. 
Atsevišķu resursu URI (novērojumiem/konceptiem) nav paredzēti tiešai pārlūka 
dereferencēšanai ar HTML/RDF atbildi. Datu izmantošana paredzēta, 
lejupielādējot RDF failu un ielādējot to analīzes rīkos vai triplestore.

---