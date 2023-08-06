# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_cloudinary_image', 'wagtail_cloudinary_image.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2',
 'cloudinary>=1.22.0',
 'django-cloudinary-storage>=0.3.0',
 'wagtail>=2.9']

setup_kwargs = {
    'name': 'wagtail-cloudinary-image',
    'version': '0.0.3',
    'description': 'Wagtail Image model that utilized django-cloudinary-storage',
    'long_description': None,
    'author': 'David Burke',
    'author_email': 'david@burkesoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
