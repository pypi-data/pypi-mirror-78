# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgcli',
 'tgcli.commands',
 'tgcli.commands.config',
 'tgcli.commands.delete',
 'tgcli.commands.etc',
 'tgcli.commands.get',
 'tgcli.commands.gsql',
 'tgcli.commands.load',
 'tgcli.tigergraph',
 'tgcli.util']

package_data = \
{'': ['*']}

install_requires = \
['pyTigerGraph>=0.0.7,<0.0.8', 'typer>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['tgcli = tgcli:tgcli']}

setup_kwargs = {
    'name': 'tigergraphcli',
    'version': '0.0.2.1',
    'description': 'CLI for TigerGraph',
    'long_description': "# TigerGraphCLI (tgcli)\n\n![PyPI Version Badge](https://img.shields.io/pypi/v/tigergraphcli)\n![Python Versions Badge](https://img.shields.io/pypi/pyversions/tigergraphcli)\n\nTigerGraphCLI is a command-line utility for interacting with [TigerGraph](https://www.tigergraph.com/) servers. It's\nbuilt on top of [pyTigerGraph](https://github.com/pyTigerGraph/pyTigerGraph).\n\nThis project is still under active development. If you find a bug or have a feature request, feel free to create a Github issue.\n\n## Installation\n\nTgcli is released on [PyPI](https://pypi.org/project/tigergraphcli/). Tgcli works best with Python 3.7+, but should work with any Python3 distribution. Installation is simple:\n`pip3 install tigergraphcli`.\n\nVerify your installation by running `tgcli version`\n\nOnce installed, get started by creating a configuration, which holds all the config and credentials needed to\nconnect to a TigerGraph server. You can do this by running `tgcli config add`. This will guide you through creating\na tgcli configuration.\n\n## Usage\n\nThere are 5 main operations that tgcli supports:\n\n1. `tgcli config`: Manages TigerGraph server configurations. Configurations are stored in a folder named `.tgcli`\nunder the home directory (ex. `~/.tgcli`)\n2. `tgcli gsql`: Runs a GSQL command against a TigerGraph server\n3. `tgcli load`: Loads vertices/edges to a TigerGraph server\n4. `tgcli get`: Retrieves data from a TigerGraph server\n5. `tgcli delete`: Delete data from a TigerGraph server.\n\nSee [usage](https://github.com/frankfka/TigerGraphCLI/blob/master/docs/USAGE.md) for detailed documentation.",
    'author': 'Frank Jia',
    'author_email': 'jiafrank98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frankfka/TigerGraphCLI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
