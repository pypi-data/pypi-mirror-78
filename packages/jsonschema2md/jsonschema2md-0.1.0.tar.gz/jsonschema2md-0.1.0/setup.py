# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jsonschema2md']
install_requires = \
['click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'jsonschema2md',
    'version': '0.1.0',
    'description': 'Convert JSON Schema to human-readable Markdown documentation',
    'long_description': '# jsonschema2md\n\n_Convert JSON Schema to human-readable Markdown documentation_\n\n',
    'author': 'Ralf Gabriels',
    'author_email': 'ralfg@hotmail.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RalfG/jsonschema2md',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
