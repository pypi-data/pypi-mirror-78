# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyml', 'jrpyml.datasets']

package_data = \
{'': ['*'], 'jrpyml': ['vignettes/*'], 'jrpyml.datasets': ['data/*']}

install_requires = \
['jrpyanalytics',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.23.4,<0.24.0',
 'scipy==1.2',
 'sklearn>=0.0.0,<0.0.1',
 'statsmodels>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'jrpyml',
    'version': '0.2.8',
    'description': 'Jumping Rivers: Machine Learning in Python',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
