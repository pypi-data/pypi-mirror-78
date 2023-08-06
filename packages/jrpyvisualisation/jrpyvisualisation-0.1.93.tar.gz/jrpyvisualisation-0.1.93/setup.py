# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyvisualisation', 'jrpyvisualisation.datasets']

package_data = \
{'': ['*'],
 'jrpyvisualisation': ['vignettes/*'],
 'jrpyvisualisation.datasets': ['data/*']}

install_requires = \
['numpy>=1.17,<2.0',
 'pandas>=0.25.0,<0.26.0',
 'plotly>=4.1,<5.0',
 'scikit-learn>=0.21.3,<0.22.0',
 'sklearn>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'jrpyvisualisation',
    'version': '0.1.93',
    'description': 'Jumping Rivers: Introduction to Visualisation in Python',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)
