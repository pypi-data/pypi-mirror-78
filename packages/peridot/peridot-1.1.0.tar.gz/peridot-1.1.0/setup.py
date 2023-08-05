# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peridot', 'peridot.version', 'peridot.version.modules']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2',
 'colorama==0.4.3',
 'perimod>=1.0.1,<2.0.0',
 'prompt_toolkit>=3.0.7,<4.0.0',
 'pygments>=2.6.1,<3.0.0',
 'xdgappdirs>=1.4.5,<2.0.0']

entry_points = \
{'console_scripts': ['peridot = peridot:main']}

setup_kwargs = {
    'name': 'peridot',
    'version': '1.1.0',
    'description': 'A strongly typed interpreted language, with type inference, implemented in Python.',
    'long_description': '# Peri.dot ([1.1.0](https://github.com/toto-bird/Peri.dot/releases/tag/1.1.0))\n\n![Peri.dot Logo](https://raw.githubusercontent.com/toto-bird/Peri.dot/master/logo.png)\n\nPeri.dot is a strongly typed interpreted language, with type inference, implemented in Python. The file extension is ".peri"\n\n\n## Setup\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management.\n\n\n```bash\npip install peridot\n```\n\n## Usage \n\n```bash\nperidot file.peri\n```\n\n## Documentation\n\n[Peri.dot Language Docs](https://toto-bird.github.io/Peri.dot-lang/)\n\n## Running Unit Tests\n\nUnit tests expect pytest.  (`pip install pytest`)\nFrom the top level directory  `pytest`\n\n## Current Features\n\n* Basic REPL\n* Types:\n    * Null/None: `Null`\n    * Numbers: `Int`, `Float`\n    * Strings: `Str`\n    * Arrays: `Array`\n    * Tuples: `Tuple`\n    * Dictionaries: `Dict`\n    * Booleans: `Bool`\n    * Functions: `Function`\n    * Built-in functions: `Built-In Function`\n    * Exceptions: `Exception`\n    * Ids: `Id`\n    * Namespaces: `Namespace`\n* Types must be explicitely cast:\n    * `1 + 1` -> `2`\n    * `1 + 1.0` -> `OperationError(\'Float can not be added to Int\')`\n* Including other files: `var operations = include(\'./operations.peri\')`\n* Variables:\n    * Creation/Initialization: `var x = 2`\n    * Assignment: `x = 5`\n    * Accessing: `x`\n* Arithmetic:\n    * Addition: `1 + 2`\n    * Subtraction: `5 - 1`\n    * Multiplication: `10 * 2`\n    * Division: `25 / 5`\n    * Exponents: `2 ^ 3`\n* Global comparisons:\n    * Equals: `==`\n    * Not Equals: `!=`\n* Numeric comparisons:\n    * Greater than: `>`\n    * Less than: `<`\n    * Greater than or equal to: `>=`\n    * Less than or equal to `<=`\n* Boolean operations: `and`, `or` and `not`\n* Functions:\n    * Creation: `var add = func(a, b) {a + b}`\n    * Calling: `add(2, 6)`\n* Built-In Functions:\n    * Printing to console: `print(\'Hello World!\')`\n    * Testing: `assert(x == 10, \'x is not 10\')`\n* Exception handler: `var x = handler {10 / 0}`\n* Assert / in-peri.dot testing: `assert(x == 9, \'x is not equal to 9\')`\n* Flow control:\n    * If statements: `if (x == 1) {var y = 3} elif (x == 2) {var y = 2} else {var y = 1}`\n    * Switch statements: `switch (var x in a) {case (x == 10) {print(\'10\')} else {print(\'Hmm...\')}}`\n    * For loops: `for (var i in [True, True, False]) {print(i)}`\n    * While loops: `while (x < 100) {x = x + 1}`\n\n## Coming Soon\n\n* Improved repl\n* Classes for general use: `var Test = class() {a = \'hello\'}`\n\n## Possible Features\n\n* Formatted strings `\'Hello World{suffix}\'`\n* More operations:\n    * Add and assign `+=`\n    * Subtract and assign `-=`\n    etc.\n',
    'author': 'Totobird',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://toto-bird.github.io/Peri.dot-lang',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
