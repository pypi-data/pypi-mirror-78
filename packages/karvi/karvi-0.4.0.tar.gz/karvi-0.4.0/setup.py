# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['karvi',
 'karvi.migrations',
 'karvi.templatetags',
 'karvi.tests',
 'karvi.tests.utils',
 'karvi.utils',
 'karvi.widgets']

package_data = \
{'': ['*'],
 'karvi': ['assets/*',
           'assets/js/*',
           'assets/js/plugins/*',
           'assets/sass/*',
           'assets/ts/*',
           'assets/ts/utils/*',
           'static/karvi/css/*',
           'static/karvi/js/*',
           'templates/karvi/addons/*',
           'templates/karvi/base/*',
           'templates/karvi/navbar/*',
           'templates/registration/*']}

install_requires = \
['django>=2.2,<2.3']

setup_kwargs = {
    'name': 'karvi',
    'version': '0.4.0',
    'description': 'A small package with custom resources for Django projects.',
    'long_description': '# Karvi\n\nA small package with some custom templates and scripts for Django projects.\n\n## Requirements\n\n-   [Python](https://www.python.org) 3.6\n-   [Django](https://www.djangoproject.com) 2.2\n\n## Projects in use\n\n-   [Bulma](https://bulma.io) 0.9\n-   [TypeScript](https://www.typescriptlang.org) 3.2\n-   [Laravel Mix](https://github.com/JeffreyWay/laravel-mix) 4.0\n-   [Yarn](https://yarnpkg.com)\n-   [Poetry](https://python-poetry.org)\n',
    'author': 'Facundo Arano',
    'author_email': 'aranofacundo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/aranofacundo/karvi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
