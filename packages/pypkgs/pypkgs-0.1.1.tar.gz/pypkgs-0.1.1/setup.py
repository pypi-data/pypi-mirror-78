# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.5,<2.0.0']

entry_points = \
{'console_scripts': ['pypkgs = pypkgs.cli:main']}

setup_kwargs = {
    'name': 'pypkgs',
    'version': '0.1.1',
    'description': 'Python package that eases the pain of concatenating Pandas categoricals!',
    'long_description': '## pypkgs \n\n![](https://github.com/TomasBeuzen/pypkgs/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/TomasBeuzen/pypkgs/branch/master/graph/badge.svg)](https://codecov.io/gh/TomasBeuzen/pypkgs) ![build](https://github.com/TomasBeuzen/pypkgs/workflows/build/badge.svg) [![Documentation Status](https://readthedocs.org/projects/pypkgs/badge/?version=latest)](https://pypkgs.readthedocs.io/en/latest/?badge=latest)\n\nPython package that eases the pain of concatenating Pandas categoricals!\n\n### Installation\n\n```\npip install -i https://test.pypi.org/simple/ pypkgs\n```\n\n### Dependencies\n\nSee [poetry.lock](poetry.lock) for a list of dependencies.\n\n### Usage\n\n```python\n>>> from pypkgs import pypkgs\n>>> import pandas as pd\n>>> a = pd.Categorical(["character", "hits", "your", "eyeballs"])\n>>> b = pd.Categorical(["but", "integer", "where it", "counts"])\n>>> pypkgs.catbind(a, b)\n[character, hits, your, eyeballs, but, integer, where it, counts]\nCategories (8, object): [but, character, counts,\neyeballs, hits, integer, where it, your]\n```\n\n### Documentation\nThe official documentation is hosted on Read the Docs: https://pypkgs.readthedocs.io/en/latest/\n\n### Credits\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Tomas Beuzen',
    'author_email': 'tomas.beuzen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TomasBeuzen/pypkgs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
