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
    'version': '0.2.0',
    'description': 'Extra tools for rdflib',
    'long_description': "# ...\n\n```bash\n# Install pipx\npip3 install --user --upgrade pipx\n\n# Run SPARQL without reasoning ...\ntime pipx run --spec yocho.rdflib-xtl rdflib-xtl sparql -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' http://xmlns.com/foaf/spec/index.rdf\n\n# Run SPARQL with reasoning ...\ntime pipx run --spec yocho.rdflib-xtl rdflib-xtl sparql --reason -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' http://xmlns.com/foaf/spec/index.rdf\n\n# Run reasoning ...\ntime pipx run --spec yocho.rdflib-xtl rdflib-xtl reason http://xmlns.com/foaf/spec/index.rdf\n```\n\n```bash\npipx run --spec yocho.rdflib-xtl rdflib-xtl sparql -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' http://xmlns.com/foaf/spec/index.rdf\n```\n\n",
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
