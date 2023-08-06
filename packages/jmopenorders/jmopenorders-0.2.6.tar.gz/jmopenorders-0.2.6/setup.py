# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jmopenorders', 'jmopenorders.api', 'jmopenorders.core']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'openpyxl>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['jmopenorders = jmopenorders.__main__:main']}

setup_kwargs = {
    'name': 'jmopenorders',
    'version': '0.2.6',
    'description': 'a generator to generate infos for the affected persm ons',
    'long_description': ' .. Copyright (c) 2019-2020 Jürgen Mülbert. All rights reserved.\n\n .. Licensed under the EUPL, Version 1.2 or – as soon they\n    will be approved by the European Commission - subsequent\n    versions of the EUPL (the "Licence");\n    You may not use this work except in compliance with the\n    Licence.\n\n .. You may obtain a copy of the Licence at:\n    https://joinup.ec.europa.eu/page/eupl-text-11-12\n\n .. Unless required by applicable law or agreed to in\n    writing, software distributed under the Licence is\n    distributed on an "AS IS" basis,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either\n    express or implied.\n    See the Licence for the specific language governing\n    permissions and limitations under the Licence.\n\n .. Lizenziert unter der EUPL, Version 1.2 oder - sobald\n    diese von der Europäischen Kommission genehmigt wurden -\n    Folgeversionen der EUPL ("Lizenz");\n    Sie dürfen dieses Werk ausschließlich gemäß\n    dieser Lizenz nutzen.\n\n .. Eine Kopie der Lizenz finden Sie hier:\n    https://joinup.ec.europa.eu/page/eupl-text-11-12\n\n .. Sofern nicht durch anwendbare Rechtsvorschriften\n    gefordert oder in schriftlicher Form vereinbart, wird\n    die unter der Lizenz verbreitete Software "so wie sie\n    ist", OHNE JEGLICHE GEWÄHRLEISTUNG ODER BEDINGUNGEN -\n    ausdrücklich oder stillschweigend - verbreitet.\n    Die sprachspezifischen Genehmigungen und Beschränkungen\n    unter der Lizenz sind dem Lizenztext zu entnehmen.\n\njmopenorders\n============\n\n\n|Gitpod| |Tests| |Code Quality| |LGTM|\xa0|Codecov| |PyPI| |Python Version| |Read the Docs|  |Black| |pre-commit| |Dependabot| |License|\n\nFeatures\n--------\n\njmopenorders is a generator to generate infos for the affected persons.\n\nGenerate from a excel-output for each service person a seperated excel file. You must the excel-file save as csv-file.\n\njmopenorders is written in `Python`_.\npython does run on almosts known platforms.\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *jmopenorders* via pip_ from `PyPI`_:\n\n.. code-block:: bash\n\n   $ pip install jmopenorders\n\n\nThe master branch represents the latest pre-release code.\n\n-   `Releases`_.\n\n-   `Milestones`_.\n\n\n\nUsage\n-----\n\n* TODO\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the EUPL-1.2_ license,\n*jmopenorders* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _EUPL-1.2: http://opensource.org/licenses/EUPL-1.2\n.. _Python: https://www.python.org\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/jmuelbert/jmopenorders/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Releases: https://github.com/jmuelbert/jmopenorders/releases\n.. _Milestones: https://github.com/jmuelbert/jmopenorders/milestones\n\n.. |Gitpod| image:: https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod\n    :target: https://gitpod.io/#https://github.com/jmuelbert/jmopenorders\n    :alt: Gitpod-Ready-Code\n\n.. |Tests| image:: https://github.com/jmuelbert/jmopenorders/workflows/Tests/badge.svg\n   :target: https://github.com/jmuelbert/jmopenorders/actions?workflow=Tests\n   :alt: Tests\n\n.. |Code Quality| image:: https://api.codacy.com/project/badge/Grade/6af827d12e264ff3bafee6b879dab554\n   :target: https://app.codacy.com/manual/jmuelbert/jmopenorders?utm_source=github.com&utm_medium=referral&utm_content=jmuelbert/jmopenorders&utm_campaign=Badge_Grade_Dashboard\n   :alt: Codacy Badge\n\n.. |LGTM| image:: https://img.shields.io/lgtm/alerts/g/jmuelbert/jmopenorders.svg?logo=lgtm&logoWidth=18\n    :target: https://lgtm.com/projects/g/jmuelbert/jmopenorders/alerts/\n    :alt: LGTM\n\n.. |Codecov| image:: https://codecov.io/gh/jmuelbert/jmopenorders/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/jmuelbert/jmopenorders\n   :alt: Codecov\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/jmopenorders.svg\n   :target: https://pypi.org/project/jmopenorders/\n   :alt: PyPI\n\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/jmopenorders\n   :target: https://pypi.org/project/jmopenorders\n   :alt: Python Version\n\n.. |Read the Docs| image:: https://readthedocs.org/projects/jmopenorders/badge/\n   :target: https://jmopenorders.readthedocs.io/\n   :alt: Read the Docs\n\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\n.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=jmuelbert/jmopenorders\n   :target: https://dependabot.com\n   :alt: Dependabot\n\n.. |License| image:: https://img.shields.io/pypi/l/jmopenorders\n   :target: LICENSE.rst\n   :alt: Project License\n',
    'author': 'Jürgen Mülbert',
    'author_email': 'juergen.muelbert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmuelbert/jmopenorders',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.10,<4.0',
}


setup(**setup_kwargs)
