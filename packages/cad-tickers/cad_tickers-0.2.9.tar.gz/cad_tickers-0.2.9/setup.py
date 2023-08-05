# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cad_tickers', 'cad_tickers.exchanges', 'cad_tickers.news', 'cad_tickers.util']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'coverage>=5.2,<6.0',
 'lxml>=4.5.2,<5.0.0',
 'pandas>=1.0.5,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'cad-tickers',
    'version': '0.2.9',
    'description': 'Various Stock Utilties Created by me',
    'long_description': "[![PyPI version](https://badge.fury.io/py/cad-tickers.svg)](https://badge.fury.io/py/cad-tickers) [![Downloads](https://pepy.tech/badge/cad-tickers)](https://pepy.tech/project/cad-tickers) [![Documentation Status](https://readthedocs.org/projects/cad-tickers/badge/?version=latest)](https://cad-tickers.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/FriendlyUser/cad_tickers/branch/master/graph/badge.svg)](https://codecov.io/gh/FriendlyUser/cad_tickers)\n \n## Cad Tickers\n\nFor the tsx searching, it was kinda tedious to test each of the possible values, as a result, only `exchanges` and `marketcap` values are validated.\n\nGiven the new redesign of the web.tmxmoney site, don't expect the existing api to work\nfor a super long period of time.\n\nSupport will be provided to the best of my ability.\n\n### How to run tests\n\n```\npytest\n```\n\n### How to deploy\n\n\n```\n# Needed for readthedocs documentation\npoetry export -f requirements.txt > requirements.txt.\n```\n\n#### Todo\n\nAdd parameters and returns, double sync with readthe docs and github pages.\n\n- [ ] Go through list in https://thecse.com/en/listings and make pandas dataframe?\nIterate until last css is no longer present\n\n- [ ] make another function that uses the new graphql api instead of the standard api.\n- [x] Convert all the Input to Parameters and output to Return\n- [x] add just read the docs\n- [x] add code coverage uploading \n- [x] news and iiroc fetching\n",
    'author': 'David Li',
    'author_email': 'davidli012345@gmail.com',
    'maintainer': 'David Li',
    'maintainer_email': 'davidli012345@gmail.com',
    'url': 'https://github.com/FriendlyUser/cad_tickers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
