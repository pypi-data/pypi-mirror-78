# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_factory', 'tests', 'tests.legacy', 'tests.pytest_factory']

package_data = \
{'': ['*']}

modules = \
['pytest', 'LICENSE', 'CHANGELOG']
install_requires = \
['factory_boy>=2.10.0', 'pytest>4.3']

entry_points = \
{'pytest11': ['factory = pytest_factory.plugin']}

setup_kwargs = {
    'name': 'pytest-factory',
    'version': '0.0.1.dev0',
    'description': 'Use factories for test setup with py.test',
    'long_description': '# pytest-factory\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/pytest-drf',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
