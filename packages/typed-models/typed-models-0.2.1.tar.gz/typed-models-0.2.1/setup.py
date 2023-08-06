# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_models', 'typed_models.fields']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'typed-models',
    'version': '0.2.1',
    'description': 'Strongly typed, lightweight, serializable models for Python',
    'long_description': "Contributing\n============\n\nContributions are welcome.\n\nGetting started\n---------------\n\nTo work on the typed-models codebase, you'll want to clone the project locally\nand install the required dependencies via `poetry <https://poetry.eustace.io>`_.\n\n.. code-block:: bash\n\n    $ git clone git@github.com:a2d24/typed-models.git\n    $ poetry install",
    'author': 'Imtiaz Mangerah',
    'author_email': 'Imtiaz_Mangerah@a2d24.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a2d24/typed-models',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
