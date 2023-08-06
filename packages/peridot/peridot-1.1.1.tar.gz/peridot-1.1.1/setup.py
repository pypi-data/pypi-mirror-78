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
{'console_scripts': ['peridot = peridot:main', 'periscope = periscope:main']}

setup_kwargs = {
    'name': 'peridot',
    'version': '1.1.1',
    'description': 'A strongly typed interpreted language, with type inference, implemented in Python.',
    'long_description': '# Peri.dot ([1.1.1](https://github.com/toto-bird/Peri.dot/releases/tag/1.1.1))\n\n![Peri.dot Logo](https://raw.githubusercontent.com/toto-bird/Peri.dot/master/logo.png)\n\n\n[Homepage](https://toto-bird.github.io/Peri.dot-lang/)<br />\n[Documentation](https://toto-bird.github.io/Peri.dot-lang/docs)<br />\n[Playground](https://toto-bird.github.io/Peri.dot-lang/playground)<br />',
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
