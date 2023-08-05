# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manage_fastapi']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['manage-fastapi = manage_fastapi.main:app']}

setup_kwargs = {
    'name': 'manage-fastapi',
    'version': '0.1.52',
    'description': 'Managing FastAPI projects made easy.',
    'long_description': '\n\n<h3 align="center">\n    <strong>Managing FastAPI projects made easy</strong>\n</h3>\n<p align="center">\n<img src="https://img.shields.io/github/issues/ycd/manage-fastapi?style=for-the-badge">\n<a href="https://github.com/ycd/manage-fastapi" target="_blank">\n    <img src="https://img.shields.io/bitbucket/pr-raw/ycd/manage-fastapi?style=for-the-badge" alt="Build">\n    <img alt="Travis (.com)" src="https://img.shields.io/travis/com/ycd/manage-fastapi?style=for-the-badge">\n</a>\n<a href="https://github.com/ycd/manage-fastapi" target="_blank">\n    <img src="https://img.shields.io/github/last-commit/ycd/manage-fastapi?style=for-the-badge" alt="Latest Commit">\n</a>\n<br />\n<a href="https://pypi.org/project/manage-fastapi" target="_blank">\n    <img src="https://img.shields.io/pypi/v/manage-fastapi?style=for-the-badge" alt="Package version">\n</a>\n    <img src="https://img.shields.io/pypi/pyversions/manage-fastapi?style=for-the-badge">\n    <img src="https://img.shields.io/github/license/ycd/manage-fastapi?style=for-the-badge">\n</p>\n\n\n---\n\n**Documentation**: View it on [website](https://ycd.github.io/manage-fastapi/)\n\n**Source Code**: View it on [Github](https://github.com/ycd/manage-fastapi/)\n\n**Installation**: `pip install manage-fastapi`\n\n---\n\n\n\n##  Features :rocket:\n\n* #### Creates customizable **project boilerplate.**\n* #### Creates customizable **app boilerplate.**\n* #### Handles the project structing for you.\n* #### Get fancy information about your Pydantic models.\n* #### Running development server.\n\n## Starting a new project\n\n<img src="docs_assets/startproject.png" width=700>\n\n\n## Example folder structure with two commands :open_file_folder:\n\n```\nmanage-fastapi startproject fastproject\nmanage-fastapi startapp v1\n```\n\n\n```\nfastproject/\n├── __init__.py\n├── main.py\n├── core\n│\xa0\xa0 ├── models\n│\xa0\xa0 │\xa0\xa0 ├── database.py\n│\xa0\xa0 │\xa0\xa0 └── __init__.py\n│\xa0\xa0 ├── schemas\n│\xa0\xa0 │\xa0\xa0 ├── __init__.py\n│\xa0\xa0 │\xa0\xa0 └── schema.py\n│\xa0\xa0 └── settings.py\n├── tests\n│\xa0\xa0 ├── __init__.py\n│\xa0\xa0 └── v1\n│\xa0\xa0     ├── __init__.py\n│\xa0\xa0     └── test_v1.py\n└── v1\n    ├── api.py\n    ├── endpoints\n    │\xa0\xa0 ├── endpoint.py\n    │\xa0\xa0 └── __init__.py\n    └── __init__.py\n```\n\n## Getting information about our Pydantic models.\n\n```\nmanage-fastapi showmodels\n```\n\n\n## With this command we are getting a fancy output of our models.\n\n```\n╔════════════════════════════════╗\n║ item.py                        ║\n║ -------                        ║\n║ ItemBase                       ║\n║ ItemCreate                     ║\n║ ItemUpdate                     ║\n║ ItemInDBBase                   ║\n║ Item                           ║\n║ ItemInDB                       ║\n╚════════════════════════════════╝\n╔════════════════════════════════╗\n║ token.py                       ║\n║ --------                       ║\n║ Token                          ║\n║ TokenPayload                   ║\n╚════════════════════════════════╝\n```\n\n\n## Installation :pushpin:\n\n`pip install manage-fastapi`\n\n\n## Release Notes :mega:\n\n### Latest Changes\n\n### 0.1.51\n\n* Little update on API template\n\n\n### 0.1.5\n\n* Added showmodels\n* Added runserver\n* Fix little bugs\n* Update docs\n\n\n### 0.1.41\n\n* Quick fix for a little bug\n\n\n### 0.1.4\n\n* Changed project architecture\n* Increased travis tests\n\n\n### 0.1.3\n\n* Make database optional\n* Now Manage FastAPI has support for MongoDB, PostgreSQL, SQLite, MySQL, Tortoise ORM\n\n### 0.1.2\n\n* Add tests\n* Fix and relocate success message \n* Add travis \n\n### 0.1.1\n\n* Added documentation\n* Fixed typos\n* Additional response for successfuly creation.\n\n### 0.1.0\n\n* Prototype of project with two functionalities.\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'ycd',
    'author_email': 'yagizcanilbey1903@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ycd/manage-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
