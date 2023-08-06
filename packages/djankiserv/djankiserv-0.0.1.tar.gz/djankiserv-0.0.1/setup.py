# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djankiserv',
 'djankiserv.api',
 'djankiserv.assets.jsonfiles',
 'djankiserv.assets.sql.sqlite3',
 'djankiserv.migrations',
 'djankiserv.sync',
 'djankiserv.unki']

package_data = \
{'': ['*']}

install_requires = \
['django-k8s>=0.2.9,<0.3.0',
 'django>=3.1,<4.0',
 'djangorestframework-simplejwt>=4.4.0,<5.0.0',
 'djangorestframework>=3.11.1,<4.0.0',
 'gunicorn>=20.0.4,<21.0.0']

setup_kwargs = {
    'name': 'djankiserv',
    'version': '0.0.1',
    'description': 'Django-based synchronisation and API server for Anki',
    'long_description': None,
    'author': 'Anton Melser',
    'author_email': 'anton@melser.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
