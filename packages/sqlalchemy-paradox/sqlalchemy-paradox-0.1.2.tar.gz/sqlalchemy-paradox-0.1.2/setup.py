# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_paradox']

package_data = \
{'': ['*']}

install_requires = \
['pyodbc>=4.0.30,<5.0.0', 'sqlalchemy>=1.3.18,<2.0.0']

entry_points = \
{'sqlalchemy.dialects': ['paradox = '
                         'sqlalchemy_paradox.pyodbc:ParadoxDialect_pyodbc',
                         'paradox.pyodbc = '
                         'sqlalchemy_paradox.pyodbc:ParadoxDialect_pyodbc']}

setup_kwargs = {
    'name': 'sqlalchemy-paradox',
    'version': '0.1.2',
    'description': 'SQLAlchemy support for BDE Paradox tables',
    'long_description': '# SQLAlchemy-Paradox\n\nA SQLAlchemy dialect for the Microsoft Paradox DB ODBC Driver\n\n## Objectives\n\nThis dialect is mainly intended to offer an easy way to access the\nParadox DB flat-file databases of older or EOL\'d application-specific\nsoftwares. It is designed for use with the ODBC driver included with\nmost versions of Microsoft Windows, `Microsoft Paradox Driver (*.db)` **ODBCJT32.DLL**.\n\n## Pre-requisites\n\n- A System or User DSN configured to use the Microsoft Paradox driver\n\n- 32-bit Python. The Microsoft Paradox driver *may* come in a 64-bit\n  version, but using it might run into the same "bittedness" issue\n  experienced with other JET-based ODBC drivers.\n\n## Co-requisites\n\nThis dialect requires SQLAlchemy and pyodbc. They are both specified as\nrequirements so `pip` will install them if they are not already in\nplace. To install separately, just:\n\n> `pip install -U SQLAlchemy pyodbc`\n\n## Installation\n\nPyPI-published version:\n\n> `pip install -U sqlalchemy-paradox`\n\nAbsolute bleeding-edge (probably buggy):\n\n> `pip install -U git+https://github.com/the-wondersmith/sqlalchemy-paradox`\n\n## Getting Started\n\nCreate an `ODBC DSN (Data Source Name)` that points to the directory\ncontaining your Paradox table files.\n\nThen, in your Python app, you can connect to the database via:\n\n```python\nimport sqlalchemy_paradox\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\n\n\ndb = create_engine("paradox+pyodbc://@your_dsn", echo=False)\nsuper_session = sessionmaker(bind=db)\nsuper_session.configure(autoflush=True, autocommit=True, expire_on_commit=True)\nsession = super_session()\n```\n\n## The SQLAlchemy Project\n\nSQLAlchemy-Paradox is based on SQLAlchemy-access, which is part of the\n[SQLAlchemy Project](https://www.sqlalchemy.org) and *tries* to adhere\nto the same standards and conventions as the core project.\n\nAt the time of this writing, it\'s unlikely that SQLAlchemy-Paradox\nactually *does* comply with the aforementioned standards and\nconventions. That will be rectified (if and when) in a future release.\n\n## Development / Bug reporting / Pull requests\n\nSQLAlchemy maintains a\n[Community Guide](https://www.sqlalchemy.org/develop.html) detailing\nguidelines on coding and participating in that project.\n\nWhile I\'m aware that this project could desperately use the\nparticipation of anyone else who actually knows what they\'re doing,\nParadox DB may be so esoteric and obscure (at the time of this writing)\nthat I wouldn\'t reasonably expect anyone to actually want to. If I am\nmistaken in that belief, *please God* submit a pull request.\n\nThis library technically *works*, but it\'s *far* from feature-complete.\n\n## License\n\nThis library is derived almost in its entirety from the\nSQLAlchemy-Access library written by\n[Gord Thompson](https://github.com/gordthompson). As such, and given\nthat SQLAlchemy-access is distributed under the\n[MIT license](https://opensource.org/licenses/MIT), this library is\nsubject to the same licensure and grant of rights as its parent works\n[SQLALchemy](https://www.sqlalchemy.org/) and\n[SQLAlchemy-Access](https://github.com/sqlalchemy/sqlalchemy-access).\n',
    'author': 'Mark S.',
    'author_email': 'developers@pawn-pay.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/the-wondersmith/sqlalchemy-paradox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
