# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toml_cli']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.7.0,<0.8.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['toml = toml_cli:main']}

setup_kwargs = {
    'name': 'toml-cli',
    'version': '0.1.3',
    'description': 'Command line interface to read and write keys/values to/from toml files',
    'long_description': '# tom-cli\n\nCommand line interface for toml files.\n\nThis can be usefull for getting or setting parts of a toml file without an editor.\nWhich can be convinient when values have to be read by a script for example in\ncontinuous development steps.\n\n\n## Install\n\n`pip install toml-cli`\n\n## Get a value\n\n`toml get --toml-path pyproject.toml tool.poetry.name`\n\n## Set a value\n\n`toml set --toml-path pyproject.toml tool.poetry.version 0.2.0`\n\n## Add a section\n\n`toml add_section --toml-path pyproject.toml tool.poetry.new_section`\n\n## Unset a value\n\n`toml unset --toml-path pyproject.toml tool.poetry.version`\n',
    'author': 'Marc Rijken',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrijken/toml-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
