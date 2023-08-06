# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beet', 'beet.contrib']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.8,<0.9',
 'click>=7.1.2,<8.0.0',
 'nbtlib>=1.8.0,<2.0.0',
 'pathspec>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['beet = beet.cli:main']}

setup_kwargs = {
    'name': 'beet',
    'version': '0.1.1',
    'description': 'A python library and toolchain for composing Minecraft pack generators',
    'long_description': '# Beet\n\n> A python library and toolchain for composing Minecraft pack generators.\n\n---\n\nLicense - [MIT](https://github.com/vberlier/beet/blob/master/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/beet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
