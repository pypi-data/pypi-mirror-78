# ...

```bash
poetry run rdflib-xtl
poetry run rdflib-xtl -vvv sparql -q 'SELECT * WHERE { ?s ?p ?o. }' --if 'turtle' ~/d.icat/rdf/foaf.ttl ~/d.icat/rdf/skos.ttl
poetry run rdflib-xtl -vvv sparql -q 'SELECT * WHERE { ?s ?p ?o. }' http://xmlns.com/foaf/spec/index.rdf
poetry run rdflib-xtl -vvv sparql -q 'SELECT * WHERE { ?s rdfs:subClassOf ?o. ?s rdfs:subClassOf foaf:Agent. }' http://xmlns.com/foaf/spec/index.rdf
```
