# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_dev_tools', 'python_dev_tools.formatters', 'python_dev_tools.linters']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=2.4.0,<3.0.0',
 'autoflake>=1.3.0,<2.0.0',
 'bandit>=1.6.0,<2.0.0',
 'black>=20.8b1,<21.0',
 'coverage>=5.0.0,<6.0.0',
 'darglint>=1.2,<2.0',
 'doc8>=0.8.0,<0.9.0',
 'flake8-2020>=1.6.0,<2.0.0',
 'flake8-bandit>=2.1.0,<3.0.0',
 'flake8-broken-line>=0.2.0,<0.3.0',
 'flake8-bugbear>=19.0,<20.0',
 'flake8-builtins>=1.4.0,<2.0.0',
 'flake8-commas>=2.0,<3.0',
 'flake8-comprehensions>=3.2.0,<4.0.0',
 'flake8-debugger>=3.2.0,<4.0.0',
 'flake8-docstrings>=1.5.0,<2.0.0',
 'flake8-eradicate>=0.3,<0.5',
 'flake8-fixme>=1.1.0,<2.0.0',
 'flake8-isort>=3.0.1,<4',
 'flake8-logging-format>=0.6.0,<0.7.0',
 'flake8-mutable>=1.2.0,<2.0.0',
 'flake8-quotes>=2.0.1,<3.0.0',
 'flake8-rst-docstrings>=0.0.12,<0.0.13',
 'flake8-string-format>=0.2,<0.3',
 'flake8-variables-names>=0.0.3,<0.0.4',
 'flake8>=3.8.0,<4.0.0',
 'isort>=4.3.5,<5.0.0',
 'mccabe>=0.6.0,<0.7.0',
 'pep8-naming>=0.9.0,<0.10.0',
 'pip>=20.2.0,<21.0.0',
 'pycodestyle>=2.5.0,<3.0.0',
 'pydocstyle>=5.0.0,<6.0.0',
 'pyflakes>=2.1.0,<3.0.0',
 'pytest-cov>=2.10.0,<3.0.0',
 'pytest>=6.0.0,<7.0.0',
 'pyupgrade>=2.1.0,<3.0.0',
 'tox-travis>=0.12,<0.13',
 'tox>=3.19.0,<4.0.0',
 'wemake-python-styleguide>=0.14.1,<0.15.0']

entry_points = \
{'console_scripts': ['whataformatter = python_dev_tools.whataformatter:main',
                     'whatalinter = python_dev_tools.whatalinter:main']}

setup_kwargs = {
    'name': 'python-dev-tools',
    'version': '2020.9.7',
    'description': 'Needed and up-to-date tools to develop in Python',
    'long_description': 'Python Dev Tools\n================\n\nNeeded and up-to-date tools to develop in Python (*WORK IN PROGRESS*)\n\n\n.. image:: https://img.shields.io/pypi/v/python_dev_tools.svg\n        :target: https://pypi.python.org/pypi/python_dev_tools\n\n.. image:: https://img.shields.io/pypi/l/python_dev_tools.svg\n        :target: https://github.com/vpoulailleau/python_dev_tools/blob/master/LICENSE\n\n.. image:: https://travis-ci.com/vpoulailleau/python-dev-tools.svg?branch=master\n        :target: https://travis-ci.com/vpoulailleau/python-dev-tools\n\n.. image:: https://readthedocs.org/projects/python-dev-tools/badge/?version=latest\n        :target: https://python-dev-tools.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://pepy.tech/badge/python-dev-tools\n        :target: https://pepy.tech/project/python-dev-tools\n        :alt: Downloads\n\n.. image:: https://api.codeclimate.com/v1/badges/282fcd71714dabd6a847/test_coverage\n        :target: https://codeclimate.com/github/vpoulailleau/python-dev-tools/test_coverage\n        :alt: Test Coverage\n\n.. image:: https://api.codeclimate.com/v1/badges/282fcd71714dabd6a847/maintainability\n        :target: https://codeclimate.com/github/vpoulailleau/python-dev-tools/maintainability\n        :alt: Maintainability\n\n.. image:: https://bettercodehub.com/edge/badge/vpoulailleau/python-dev-tools?branch=master\n        :target: https://bettercodehub.com/results/vpoulailleau/python-dev-tools\n        :alt: Maintainability\n\n.. image:: https://img.shields.io/lgtm/grade/python/g/vpoulailleau/python-dev-tools.svg?logo=lgtm&logoWidth=1\n        :target: https://lgtm.com/projects/g/vpoulailleau/python-dev-tools/context:python\n        :alt: Maintainability\n\nDocumentation\n-------------\n\nThe full documentation can be read at https://python-dev-tools.readthedocs.io.\n\nInstallation\n------------\n\nIn a terminal, run:\n\n.. code-block:: console\n\n    $ python3 -m pip install python-dev-tools --user --upgrade\n\nFull documentation on installation: https://python-dev-tools.readthedocs.io/en/latest/installation.html\n\nThat\'s it! Use the provided linter (``whatalinter``), formatter (``whataformatter``) and\nprecommit hook (TODO) where applicable.\n\nInstallation with Visual Studio Code\n------------------------------------\n\n* Follow the installation procedure for python-dev-tools\n* Be sure to have the official Python extension installed in VS Code\n* Open VS Code from within your activated virtual environment (in fact, make sure that \n  ``whatalinter_vscode`` is in your ``PYTHON_PATH``)\n* In VS Code, open settings (F1 key, then type "Open Settings (JSON)",\n  then enter)\n* Add in the opened JSON file (before the closing ``}``):\n\n.. code:: javascript\n\n    "python.linting.enabled": true,\n    "python.linting.flake8Enabled": true,\n    "python.linting.flake8Path": "whatalinter_vscode",\n    "python.formatting.provider": "black",\n    "python.formatting.blackPath": "black",\n    "python.formatting.blackArgs": [],\n\nFeatures\n--------\n\nIntegrate features of commonly used tools. This package provides usual\ndependencies to develop Python software.\n\n* Simple linter\n\n  * ``whatalinter a_python_file.py`` lints a_python_file.py\n  * output is compatible with the one of flake8 for easy integration in text editors\n    and IDE\n  * based on flake8 and plugins: https://gitlab.com/pycqa/flake8\n\n    * darglint: https://github.com/terrencepreilly/darglint\n    * flake8-2020: https://github.com/asottile/flake8-2020\n    * flake8-bandit: https://github.com/tylerwince/flake8-bandit\n    * flake8-broken-line: https://github.com/sobolevn/flake8-broken-line\n    * flake8-bugbear: https://github.com/PyCQA/flake8-bugbear\n    * flake8-builtins: https://github.com/gforcada/flake8-builtins\n    * flake8-commas: https://github.com/PyCQA/flake8-commas/\n    * flake8-comprehensions: https://github.com/adamchainz/flake8-comprehensions\n    * flake8-debugger: https://github.com/JBKahn/flake8-debugger\n    * flake8-docstrings: https://gitlab.com/pycqa/flake8-docstrings\n    * flake8-eradicate: https://github.com/sobolevn/flake8-eradicate\n    * flake8-fixme: https://github.com/tommilligan/flake8-fixme\n    * flake8-isort: https://github.com/gforcada/flake8-isort\n    * flake8-logging-format: https://github.com/globality-corp/flake8-logging-format\n    * flake8-mutable: https://github.com/ebeweber/flake8-mutable\n    * flake8-quotes: https://github.com/zheller/flake8-quotes/\n    * flake8-rst-docstrings: https://github.com/peterjc/flake8-rst-docstrings\n    * flake8-string-format: https://github.com/xZise/flake8-string-format\n    * flake8-variables-names: https://github.com/best-doctor/flake8-variables-names\n    * pep8-naming: https://github.com/PyCQA/pep8-naming\n    * wemake-python-styleguide: https://github.com/wemake-services/wemake-python-styleguide\n\n* Simple formatter\n\n  * ``whataformatter a_python_file.py`` formats a_python_file.py\n  * based on\n\n    * autoflake: https://github.com/myint/autoflake\n    * black: https://github.com/python/black\n    * pyupgrade: https://github.com/asottile/pyupgrade\n\n* Simple precommit hook\n\n  * TODO\n\nLicense\n-------\n\nBSD 3-Clause license, feel free to contribute: https://python-dev-tools.readthedocs.io/en/latest/contributing.html.\n\nTODO\n----\n\n* documentation\n* precommit\n\nChangelog\n---------\n\n2020.9.7\n^^^^^^^^\n\n* Remove E203 in ``flake8`` for ``black`` compatibility\n\n2020.9.4\n^^^^^^^^\n\n* Add ``whatalinter_vscode`` for Visual Studio Code integration\n\n2020.9.2\n^^^^^^^^\n\n* Remove some warnings of ``wemake-python-styleguide``, for instance allow f-strings\n\n2020.9.1\n^^^^^^^^\n\n* Use ``poetry``\n* Remove redundant linters\n* Change max line length to 88 (default value of ``black``)\n* Replace ``pydocstyle`` with ``flake8-docstrings``\n* Add ``wemake-python-styleguide``\n\n2019.10.22\n^^^^^^^^^^\n\n* Add ``flake8-2020`` linter\n\n2019.07.21\n^^^^^^^^^^\n\n* Add ``--quiet`` and ``--diff`` flags to ``whataformatter`` for VS Code compatibility\n\n2019.07.20\n^^^^^^^^^^\n\n* Add ``black`` formatter\n* Add ``autoflake`` formatter\n* Add ``pyupgrade`` formatter\n\n2019.04.08\n^^^^^^^^^^\n\n* Add ``flake8`` linter\n* Add ``flake8-isort`` linter\n* Add ``pep8-naming`` linter\n* Add ``flake8-comprehensions`` linter\n* Add ``flake8-logging-format`` linter\n* Add ``flake8-bugbear`` linter\n* Add ``flake8-builtins`` linter\n* Add ``flake8-broken-line`` linter\n* Add ``flake8-fixme`` linter\n* Add ``flake8-mutable`` linter\n* Add ``flake8-debugger`` linter\n* Add ``flake8-variables-names`` linter\n* Add ``flake8-bandit`` linter\n\n2019.03.02\n^^^^^^^^^^\n\n* Add ``pydocstyle`` linter\n\n2019.03.01\n^^^^^^^^^^\n\n* Add McCabe complexity checker\n\n2019.02.26\n^^^^^^^^^^\n\n* Add ``pyflakes`` linter\n* Add ``pycodestyle`` linter\n\n2019.02.23\n^^^^^^^^^^\n\n* First release on PyPI.\n',
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vpoulailleau/python-dev-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
