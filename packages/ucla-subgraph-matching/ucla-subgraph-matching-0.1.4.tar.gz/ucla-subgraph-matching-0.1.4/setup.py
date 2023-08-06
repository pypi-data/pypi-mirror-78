# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uclasm', 'uclasm.counting', 'uclasm.filters', 'uclasm.utils']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.4,<3.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.1,<2.0.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'ucla-subgraph-matching',
    'version': '0.1.4',
    'description': '',
    'long_description': '<div align="center">\n<img src="logo.png" alt="logo">\n</div>\n\n<h2 align="center">Pattern matching in graphs</h2>\n\n<div align="center">\n<a href="https://zenodo.org/badge/latestdoi/148378128"><img alt="PyPI Version" src="https://zenodo.org/badge/148378128.svg"></a>\n</div>\n\n<!-- <div align="center">\n<a href="https://pypi.org/project/kaczmarz-algorithms/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/kaczmarz-algorithms.svg"></a>\n<a href="https://pypi.org/project/kaczmarz-algorithms/"><img alt="Supported Python Versions" src="https://img.shields.io/pypi/pyversions/kaczmarz-algorithms.svg"></a>\n<a href="https://github.com/jdmoorman/kaczmarz-algorithms/actions"><img alt="Build Status" src="https://github.com/jdmoorman/kaczmarz-algorithms/workflows/CI/badge.svg"></a>\n<a href="https://codecov.io/gh/jdmoorman/kaczmarz-algorithms"><img alt="Code Coverage" src="https://codecov.io/gh/jdmoorman/kaczmarz-algorithms/branch/master/graph/badge.svg"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</div> -->\n',
    'author': 'Jacob Moorman',
    'author_email': 'jacob@moorman.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdmoorman/uclasm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
