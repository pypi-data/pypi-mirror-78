# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peridot_periscope', 'peridot_periscope.version']

package_data = \
{'': ['*']}

install_requires = \
['peridot>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['periscope = peridot_periscope:main']}

setup_kwargs = {
    'name': 'peridot-periscope',
    'version': '1.0.0',
    'description': 'Unit testing framework for the Peri.dot Programming Language',
    'long_description': "# Periscope (1.1)\n\n![Periscope Logo](https://raw.githubusercontent.com/toto-bird/Periscope/master/logo.png)\n\n### Usage:\nPeri.dot\n```\nvar periscope = include('periscope')\n\nvar pscope_add() -> Null {\n    return(periscope.skip(\n        'Out of date'\n    ))\n}\n\nvar pscope_sub() -> Null {\n    assert(10 - 5 == 5)\n\n    return(Null)\n}\n\nvar pscope_mul() -> Null {\n    assert(10 - 1 == 10, 'Hmm. Somethings not right')\n\n    return(Null)\n}\n```\n\nBash\n```bash\n# Test files\nperiscope peritests/*\n\n# More help\nperiscope -h\n```\n",
    'author': 'Totobird',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
