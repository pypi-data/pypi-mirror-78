# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yocho', 'yocho.rdflib_xtl']

package_data = \
{'': ['*']}

install_requires = \
['owlrl>=5.2.1,<6.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'rdflib-jsonld>=0.5.0,<0.6.0',
 'rdflib>=5.0.0,<6.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['rdflib-xtl = yocho.rdflib_xtl.cli:main']}

setup_kwargs = {
    'name': 'yocho.rdflib-xtl',
    'version': '0.1.0',
    'description': 'Extra tools for rdflib',
    'long_description': "# ...\n\n```bash\npoetry run rdflib-xtl\npoetry run rdflib-xtl -vvv sparql -q 'SELECT * WHERE { ?s ?p ?o. }' --if 'turtle' ~/d.icat/rdf/foaf.ttl ~/d.icat/rdf/skos.ttl\npoetry run rdflib-xtl -vvv sparql -q 'SELECT * WHERE { ?s ?p ?o. }' http://xmlns.com/foaf/spec/index.rdf\npoetry run rdflib-xtl -vvv sparql -q 'SELECT * WHERE { ?s rdfs:subClassOf ?o. ?s rdfs:subClassOf foaf:Agent. }' http://xmlns.com/foaf/spec/index.rdf\n```\n",
    'author': 'Iwan Aucamp',
    'author_email': 'aucampia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
