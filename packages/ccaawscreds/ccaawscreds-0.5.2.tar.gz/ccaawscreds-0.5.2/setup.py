# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccaawscreds']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.48,<2.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['awskey = ccaawscreds.credentials:awsK',
                     'awspw = ccaawscreds.credentials:awsPW',
                     'genpw = ccaawscreds.credentials:genPW']}

setup_kwargs = {
    'name': 'ccaawscreds',
    'version': '0.5.2',
    'description': 'update AWS console PW, rotate Access Keys, generate random passwords.',
    'long_description': None,
    'author': 'ccdale',
    'author_email': 'chris.charles.allison@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
