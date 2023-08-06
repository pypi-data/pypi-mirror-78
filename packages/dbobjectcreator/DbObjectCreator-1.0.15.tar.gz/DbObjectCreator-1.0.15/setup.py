# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbobjectcreator']

package_data = \
{'': ['*']}

install_requires = \
['Cython',
 'PyMySQL',
 'PyNaCl',
 'SQLAlchemy',
 'bcrypt',
 'cffi',
 'cryptography',
 'importlib_metadata',
 'numpy',
 'pandas',
 'paramiko',
 'psycopg2',
 'pycparser',
 'pymssql',
 'python-dateutil',
 'pytz',
 'six',
 'sshtunnel',
 'wheel']

setup_kwargs = {
    'name': 'dbobjectcreator',
    'version': '1.0.15',
    'description': 'A database object creator',
    'long_description': '# Database Object Creator (D.O.C.)\nThis library provides a method of creating database connector objects for quick and easy access to multiple\ndatabases (both types and servers).\n\n---\n\n## DOC Setup\nThis library can be installed via Pypi.org[https://pypi.org/project/DbObjectCreator/] or locally:\n\nRun `pip install Cython` before proceeding with either install. This package is required prior to installing this library.\nThis library can now be installed by running `pip install DbObjectCreator`\n\n## DOC Usage\n1. Import the library into your project using `from DbObjectCreator import DbObjectCreator`\n2. Create a new DbObject using `new_db = DbObjectCreator.DbObject()`\n3. new_db can now be used to call multiple methods against the database.\n\n\nThis library supports both Windows and OSX architecture. If installing on OSX you will need FreeTDS installed.\n',
    'author': 'Gary Haag',
    'author_email': 'haagimus@gmail.com',
    'maintainer': 'Gary Haag',
    'maintainer_email': 'haagimus@gmail.com',
    'url': 'https://github.com/Haagimus/DbObjectCreator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
