# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iprestrict',
 'iprestrict.management',
 'iprestrict.management.commands',
 'iprestrict.migrations']

package_data = \
{'': ['*'],
 'iprestrict': ['static/css/*',
                'static/javascript/lib/*',
                'templates/*',
                'templates/iprestrict/*']}

extras_require = \
{'geoip': ['pycountry>=20.7.3,<21.0.0', 'geoip2>=4.0.2,<5.0.0']}

setup_kwargs = {
    'name': 'django-iprestrict-redux',
    'version': '1.9.0',
    'description': 'Django app + middleware to restrict access to all or sections of a Django project by client IP ranges',
    'long_description': None,
    'author': 'Tamas Szabo',
    'author_email': 'me@tamas-szabo.com',
    'maintainer': 'Tamas Szabo',
    'maintainer_email': 'me@tamas-szabo.com',
    'url': 'https://github.com/sztamas/django-iprestrict-redux',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
