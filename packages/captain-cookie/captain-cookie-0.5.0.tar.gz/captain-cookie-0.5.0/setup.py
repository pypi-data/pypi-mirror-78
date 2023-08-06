# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['captain_cookie',
 'captain_cookie.templates.default.hooks',
 'captain_cookie.templates.default.{{cookiecutter.project_slug}}',
 'captain_cookie.templates.default.{{cookiecutter.project_slug}}.src.{{cookiecutter.project_slug}}',
 'captain_cookie.templates.default.{{cookiecutter.project_slug}}.tests']

package_data = \
{'': ['*'],
 'captain_cookie': ['templates/default/*'],
 'captain_cookie.templates.default.{{cookiecutter.project_slug}}': ['.vscode/*',
                                                                    'ci/*',
                                                                    'docs/*',
                                                                    'docs/apidoc/*',
                                                                    'docs/contributing/*',
                                                                    'docs/css/*',
                                                                    'docs/js/*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['captain-cookie = captain_cookie:run']}

setup_kwargs = {
    'name': 'captain-cookie',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'gcharbon',
    'author_email': 'guillaume.charbonnier@capgemini.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
