# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typeddfs']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1,<2',
 'natsort>=7,<8',
 'pandas>=1.1,<2.0',
 'tables>=3.6,<4.0']

setup_kwargs = {
    'name': 'typeddfs',
    'version': '0.3.0',
    'description': 'Pandas DataFrame subclasses that enforce structure and can self-organize.',
    'long_description': "# Typed DataFrames\n\n[![Latest version on PyPi](https://badge.fury.io/py/typeddfs.svg)](https://pypi.org/project/typeddfs/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/typeddfs.svg)](https://pypi.org/project/typeddfs/)\n[![Documentation status](https://readthedocs.org/projects/typed-dfs/badge/?version=latest&style=flat-square)](https://readthedocs.org/projects/typed-dfs)\n[![Build & test](https://github.com/dmyersturnbull/typed-dfs/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/typed-dfs/actions)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Build status](https://img.shields.io/pypi/status/typeddfs)](https://pypi.org/project/typeddfs/)\n[![Maintainability](https://api.codeclimate.com/v1/badges/6b804351b6ba5e7694af/maintainability)](https://codeclimate.com/github/dmyersturnbull/typed-dfs/maintainability)\n[![Coverage Status](https://coveralls.io/repos/github/dmyersturnbull/typed-dfs/badge.svg?branch=master)](https://coveralls.io/github/dmyersturnbull/typed-dfs?branch=master)\n\nPandas DataFrame subclasses that enforce structure and can self-organize.\nBecause your functions can’t exactly accept _any_  DataFrame.\n\nThe subclassed DataFrames can have required and/or optional columns and indices,\nand support custom requirements.\nColumns are automatically turned into indices,\nwhich means **`read_csv` and `to_csv` are always inverses**.\n`MyDf.read_csv(mydf.to_csv())` is just `mydf`.\n\nThe DataFrames will display nicely in Jupyter notebooks,\nand a few convenience methods are added, such as `sort_natural` and `drop_cols`.\n**[See the docs](https://typed-dfs.readthedocs.io/en/stable/)** for more information.\n\nSimple example for a CSV like this:\n\n| key   | value  | note |\n| ----- | ------ | ---- |\n| abc   | 123    | ?    |\n\n```python\nfrom typeddfs import TypedDfs\n\n# Build me a Key-Value-Note class!\nKeyValue = (\n    TypedDfs.typed('KeyValue')   # typed means enforced requirements\n    .require('key', index=True)  # automagically make this an index\n    .require('value')            # required\n    .reserve('note')             # permitted but not required\n    .strict()                    # don't allow other columns\n).build()\n\n# This will self-organize and use 'key' as the index:\ndf = KeyValue.read_csv('example.csv')\n\n# For fun, let's write it and read it back:\ndf.to_csv('remke.csv')\ndf = KeyValue('remake.csv')\nprint(df.index_names(), df.column_names())  # ['key'], ['value', 'note']\n\n# And now, we can type a function to require a KeyValue,\n# and let it raise an `InvalidDfError` (here, a `MissingColumnError`):\ndef my_special_function(df: KeyValue) -> float:\n    return KeyValue(df)['value'].sum()\n```\n\nAll of the normal DataFrame methods are available.\nUse `.untyped()` or `.vanilla()` to make a detyped copy that doesn't enforce requirements.\n\n\n[New issues](https://github.com/dmyersturnbull/typed-dfs/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/typed-dfs/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n",
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'dmyersturnbull',
    'maintainer_email': None,
    'url': 'https://github.com/kokellab/typed-dfs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
