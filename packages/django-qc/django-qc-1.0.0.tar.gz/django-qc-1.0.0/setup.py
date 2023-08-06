# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_qc']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-qc',
    'version': '1.0.0',
    'description': 'DB utility to help you catch query inefficiencies in Django.',
    'long_description': "![https://pypi.org/project/django-qc/](https://img.shields.io/pypi/v/django-qc.svg)\n![https://pypi.org/project/django-qc/](https://img.shields.io/pypi/pyversions/django-qc.svg)\n![https://pypi.python.org/pypi/django-qc](https://img.shields.io/pypi/djversions/django-qc.svg)\n![https://codecov.io/gh/sondrelg/django-query-counter](https://codecov.io/gh/sondrelg/django-query-counter/branch/master/graph/badge.svg)\n![https://pypi.org/project/django-qc/](https://img.shields.io/badge/code%20style-black-000000.svg)\n![https://github.com/pre-commit/pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)\n\n## Django query counter - simple query debugging\n\nLets you easily catch and fix database query inefficiencies during development by decorating any function or method.\n\n![Query counter](https://raw.githubusercontent.com/sondrelg/django-query-counter/master/docs/comments.gif)\n\nThe main potential drawback of seeing query data in your code is that commits can become cluttered. We therefore recommend pairing django-qc with a [pre-commit hook for removing the comments](https://github.com/sondrelg/remove-query-counts) before they are ever even committed.\n\n## Installation\n\nInstall using pip:\n\n    pip install django-qc\n\n## Settings\n\nThere's only one setting to configure, but it is required:\n\n```python\nDB_HELPER {\n    'DEBUG': DEBUG\n}\n```\n\nDecorator functions will not do anything if debug is `False`, and by design does not allow a debug value of `True` if the general Django debug value is `False`, as this is intended as a development aid only.\n",
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sondrelg/django-query-counter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
