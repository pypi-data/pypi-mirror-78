# ...

```bash
# Install pipx
pip3 install --user --upgrade pipx

# Run SPARQL without reasoning ...
time pipx run --spec yocho.rdflib-xtl rdflib-xtl sparql -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' http://xmlns.com/foaf/spec/index.rdf

# Run SPARQL with reasoning ...
time pipx run --spec yocho.rdflib-xtl rdflib-xtl sparql --reason -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' http://xmlns.com/foaf/spec/index.rdf

# Run reasoning ...
time pipx run --spec yocho.rdflib-xtl rdflib-xtl reason http://xmlns.com/foaf/spec/index.rdf
```

```bash
pipx run --spec yocho.rdflib-xtl rdflib-xtl sparql -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' http://xmlns.com/foaf/spec/index.rdf
```

