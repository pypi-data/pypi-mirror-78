# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypotonic']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.9',
 'beautifulsoup4>=4.7.1',
 'html5lib>=1.0.1',
 'jsonpath-ng>=1.5.1',
 'more_itertools>=6.0.0']

setup_kwargs = {
    'name': 'hypotonic',
    'version': '0.0.12',
    'description': 'Fast asynchronous web scraper with minimalist API.',
    'long_description': "# Hypotonic\n\nFast asynchronous web scraper with minimalist API inspired by awesome [node-osmosis](https://github.com/rchipka/node-osmosis).\n\nHypotonic provides SQLAlchemy-like command chaining DSL to define HTML scrapers. Everything is executed asynchronously via `asyncio` and all dependencies are pure Python. Supports querying by CSS selectors with Scrapy's pseudo-attributes. XPath is not supported due to `libxml` requirement.\n\nHypotonic does not natively execute JavaScript on websites and it is recommended to use [prerender](https://prerender.com).\n\n## Installing\n\nHypotonic requires Python 3.6+.\n\n`pip install hypotonic`\n\n## Example\n\n```python\nfrom hypotonic import Hypotonic\n\ndata, errors = (\n  Hypotonic()\n    .get('http://books.toscrape.com/')\n    .paginate('.next a::attr(href)', 5)\n    .find('.product_pod h3')\n    .set('title')\n    .follow('a::attr(href)')\n    .set({'price': '.price_color',\n          'availability': 'p.availability'})\n    .data()\n)\n```\n",
    'author': 'Martin Scavnicky',
    'author_email': 'martin.scavnicky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mscavnicky/hypotonic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
