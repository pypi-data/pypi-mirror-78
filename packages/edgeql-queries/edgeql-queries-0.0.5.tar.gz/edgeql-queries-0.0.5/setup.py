# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edgeql_queries',
 'edgeql_queries.contrib',
 'edgeql_queries.contrib.aiosql',
 'edgeql_queries.executors']

package_data = \
{'': ['*']}

install_requires = \
['edgedb>=0.9.0']

setup_kwargs = {
    'name': 'edgeql-queries',
    'version': '0.0.5',
    'description': 'Simple EdgeQL in Python.',
    'long_description': '<h1 align="center">edgeql-queries</h1>\n<p align="center">\n    <em>Simple EdgeQL in Python.</em>\n</p>\n<p align="center">\n    <a href=https://github.com/nsidnev/edgeql-queries>\n        <img src=https://github.com/nsidnev/edgeql-queries/workflows/Tests/badge.svg alt="Tests" />\n    </a>\n    <a href=https://github.com/nsidnev/edgeql-queries>\n        <img src=https://github.com/nsidnev/edgeql-queries/workflows/Styles/badge.svg alt="Styles" />\n    </a>\n    <a href="https://codecov.io/gh/nsidnev/edgeql-queries">\n        <img src="https://codecov.io/gh/nsidnev/edgeql-queries/branch/master/graph/badge.svg" alt="Coverage" />\n    </a>\n    <a href="https://github.com/ambv/black">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style" />\n    </a>\n    <a href="https://github.com/wemake-services/wemake-python-styleguide">\n        <img src="https://img.shields.io/badge/style-wemake-000000.svg" alt="WPS Linter"/>\n    </a>\n    <a href="https://github.com/nsidnev/edgeql-queries/blob/master/LICENSE">\n        <img src="https://img.shields.io/badge/License-FreeBSD-blue" alt="License" />\n    </a>\n    <a href="https://pypi.org/project/edgeql-queries/">\n        <img src="https://badge.fury.io/py/edgeql-queries.svg" alt="Package version" />\n    </a>\n</p>\n\n---\n\n**Documentation**: https://nsidnev.github.io/edgeql-queries/\n\n## Requirements\n\n`edgeql-queries` requires only the [EdgeDB driver for Python](https://github.com/edgedb/edgedb-python).\n\n## Credits\n\nThis project is inspired by [aiosql](https://github.com/nackjicholson/aiosql)\nproject and is based on it\'s source code.\n\n## License\n\nThis project is licensed under the terms of the FreeBSD license.\n',
    'author': 'Nik Sidnev',
    'author_email': 'sidnev.nick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nsidnev/edgeql-queries',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
