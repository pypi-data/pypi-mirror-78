# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jsonschema2md']
install_requires = \
['click>=7,<8']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1,<2']}

entry_points = \
{'console_scripts': ['jsonschema2md = jsonschema2md:main']}

setup_kwargs = {
    'name': 'jsonschema2md',
    'version': '0.1.1',
    'description': 'Convert JSON Schema to human-readable Markdown documentation',
    'long_description': '# jsonschema2md\n\n[![](https://flat.badgen.net/pypi/v/jsonschema2md?icon=pypi)](https://pypi.org/project/jsonschema2md)\n[![](https://flat.badgen.net/github/release/ralfg/jsonschema2md)](https://github.com/ralfg/jsonschema2md/releases)\n[![](https://flat.badgen.net/github/checks/ralfg/jsonschema2md/)](https://github.com/ralfg/jsonschema2md/actions)\n[![](https://flat.badgen.net/codecov/c/github/ralfg/jsonschema2md)](https://codecov.io/gh/RalfG/jsonschema2md)\n![](https://flat.badgen.net/github/last-commit/ralfg/jsonschema2md)\n![](https://flat.badgen.net/github/license/ralfg/jsonschema2md)\n\n\n*Convert JSON Schemas to simple, human-readable Markdown documentation.*\n\n---\n\nFor example:\n```json\n{\n    "$id": "https://example.com/person.schema.json",\n    "$schema": "http://json-schema.org/draft-07/schema#",\n    "title": "Person",\n    "description": "JSON Schema for a person object.",\n    "type": "object",\n    "properties": {\n      "firstName": {\n        "type": "string",\n        "description": "The person\'s first name."\n      },\n      "lastName": {\n        "type": "string",\n        "description": "The person\'s last name."\n      }\n    }\n  }\n```\n\nwill be converted to:\n\n> # Person\n> *JSON Schema for a person object.*\n> ## Properties\n>\n> - **`firstName`** *(string)*: The person\'s first name.\n> - **`lastName`** *(string)*: The person\'s last name.\n\nSee the [examples](https://github.com/RalfG/jsonschema2md/tree/master/examples)\ndirectory for more elaborate examples.\n\n---\n\n## Installation\n\nInstall with pip\n```sh\n$ pip install jsonschema2md\n```\n\n\n## Usage\n\n### From the CLI\n\n```sh\n$ jsonschema2md <input.json> <output.md>\n```\n\n\n### From Python\n\n```python\nimport jsonschema2md\nparser = jsonschema2md.Parser()\nmd_lines = parser.parse_schema(json.load(input_json))\n```\n\n\n## Contributing\n\nBugs, questions or suggestions? Feel free to post an issue in the\n[issue tracker](https://github.com/RalfG/jsonschema2md/issues/) or to make a pull\nrequest! See\n[Contributing.md](https://github.com/RalfG/jsonschema2md/blob/master/CONTRIBUTING.md)\nfor more info.\n\n\n## Changelog\n\nSee [Changelog.md](https://github.com/RalfG/jsonschema2md/blob/master/CHANGELOG.md).\n',
    'author': 'Ralf Gabriels',
    'author_email': 'ralfg@hotmail.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RalfG/jsonschema2md',
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
