# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['universal', 'universal.algos', 'universal.algos.ternary']

package_data = \
{'': ['*'], 'universal': ['data/*']}

install_requires = \
['cvxopt>=1.2.5,<2.0.0',
 'matplotlib>=3.3.1,<4.0.0',
 'pandas-datareader>=0.9.0,<0.10.0',
 'pandas>=1.1.1,<2.0.0',
 'plotly>=4.9.0,<5.0.0',
 'requests>=2.24.0,<3.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.5.2,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'statsmodels>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'universal-portfolios',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Marigold',
    'author_email': 'mojmir.vinkler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
