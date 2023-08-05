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
    'version': '0.4.1',
    'description': 'Collection of algorithms for online portfolio selection',
    'long_description': "# universal-portfolios\n\nThe purpose of this package is to put together different online portfolio selection algorithms and provide unified tools for their analysis. If you do not know what online portfolio is, look at [Ernest Chan blog](http://epchan.blogspot.cz/2007/01/universal-portfolios.html), [CASTrader](http://www.castrader.com/2006/11/universal_portf.html) or a recent [survey by Bin Li and Steven C. H. Hoi](http://arxiv.org/abs/1212.2129).\n\nIn short, the purpose of online portfolio is to _choose portfolio weights in every period to maximize its final wealth_. Examples of such portfolios could be [Markowitz portfolio](http://en.wikipedia.org/wiki/Modern_portfolio_theory) or [Universal portfolio](http://en.wikipedia.org/wiki/Universal_portfolio_algorithm). Currently there is an active research in the are of online portfolios and even though its results are mostly theoretic, algorithms for practical use starts to appear.\n\nSeveral algorithms from the literature are currently implemented, based on the available literature and my understanding. Contributions or corrections are more than welcomed.\n\n## Resources\n\nThere is an [IPython notebook](http://nbviewer.ipython.org/github/Marigold/universal-portfolios/blob/master/On-line%20portfolios.ipynb) explaining the basic use of the library. Paul Perry followed up on this and made a [comparison of all algorithms](http://nbviewer.ipython.org/github/paulperry/quant/blob/master/OLPS_Comparison.ipynb) on more recent ETF datasets. Also see the most recent [notebook about modern portfolio theory](http://nbviewer.ipython.org/github/Marigold/universal-portfolios/blob/master/modern-portfolio-theory.ipynb). There's also an interesting discussion about this on [Quantopian](https://www.quantopian.com/posts/comparing-olps-algorithms-olmar-up-et-al-dot-on-etfs#553a704e7c9031e3c70003a9).\n\nThe original authors of some of the algorithms recently published their own implementation on github - [On-Line Portfolio Selection Toolbox](https://github.com/OLPS/OLPS) in MATLAB.\n\nIf you are more into R or just looking for a good resource about Universal Portfolios, check out blog and package [logopt](http://optimallog.blogspot.cz/) by Marc Delvaux.\n\nIf you don't want to install the package locally, you can run both notebooks with Binder - [modern-portfolio-theory.ipynb ![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Marigold/universal-portfolios/master?filepath=modern-portfolio-theory.ipynb) or [On-line portfolios.ipynb ![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Marigold/universal-portfolios/master?filepath=On-line%20portfolios.ipynb)\n\n## Installation\n\n```\npip install universal-portfolios\n```\n\n## Development\n\nIt uses poetry to manage dependencies. Run `poetry install` to install virtual environment and then `poetry shell` to launch it.\n\nExporting dependencies to `requirements.txt` file is done via\n\n```\npoetry export --without-hashes -f requirements.txt > requirements.txt\npoetry export --dev --without-hashes -f requirements.txt > test-requirements.txt\n```\n\nthis is needed for mybinder.org.\n\n## Tests\n\n```\npoetry run python -m pytest --capture=no --ff -x tests/ -k test_bias\n```\n",
    'author': 'Marigold',
    'author_email': 'mojmir.vinkler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Marigold/universal-portfolios',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
