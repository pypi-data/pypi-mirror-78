# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lk_qtquick_scaffold', 'lk_qtquick_scaffold.control']

package_data = \
{'': ['*'], 'lk_qtquick_scaffold': ['docs/*', 'qml/sample/*', 'resources/*']}

install_requires = \
['lk-utils>=1.3.1,<2.0.0', 'pyside2>=5.15.0,<6.0.0']

setup_kwargs = {
    'name': 'lk-qtquick-scaffold',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
