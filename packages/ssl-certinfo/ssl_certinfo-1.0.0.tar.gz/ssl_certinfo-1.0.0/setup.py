# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssl_certinfo']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'pyopenssl', 'pyyaml', 'tabulate', 'tqdm']

entry_points = \
{'console_scripts': ['ssl_certinfo = ssl_certinfo.cli:main']}

setup_kwargs = {
    'name': 'ssl-certinfo',
    'version': '1.0.0',
    'description': 'SSL CertInfo collects information about SSL certificates from a set of hosts.',
    'long_description': '============\nSSL CertInfo\n============\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - build\n      - |travis|\n    * - quality\n      - |codacy| |codeclimate| |sonar-qg| |sonar-rel|\n    * - coverage\n      - |coveralls| |codecov| |codeclimate-cov|\n    * - dependencies\n      - |pyup| |pyup-p3| |requires|\n    * - package\n      - |version| |pyversions| |downloads|\n\n\n.. |travis| image:: https://img.shields.io/travis/stdtom/ssl_certinfo/master.svg?logo=travis\n   :target: https://travis-ci.com/stdtom/ssl_certinfo\n   :alt: Travis Build Status\n\n.. |codacy| image:: https://api.codacy.com/project/badge/Grade/589c03a215ec4ddbb0085b523a857e55\n   :target: https://www.codacy.com/manual/stdtom/ssl_certinfo\n   :alt: Codacy Grade\n\n.. |codeclimate| image:: https://api.codeclimate.com/v1/badges/1ed86e874b3c68672c5c/maintainability\n   :target: https://codeclimate.com/github/stdtom/ssl_certinfo/maintainability\n   :alt: Code Climate Maintainability\n\n.. |sonar-qg| image:: https://sonarcloud.io/api/project_badges/measure?project=stdtom_ssl_certinfo&metric=alert_status\n   :target: https://sonarcloud.io/dashboard?id=stdtom_ssl_certinfo\n   :alt: Sonar Quality Gate Status\n\n.. |sonar-rel| image:: https://sonarcloud.io/api/project_badges/measure?project=stdtom_ssl_certinfo&metric=reliability_rating\n   :target: https://sonarcloud.io/dashboard?id=stdtom_ssl_certinfo\n   :alt: Sonar Reliability Rating\n\n.. |coveralls| image:: https://coveralls.io/repos/github/stdtom/ssl_certinfo/badge.svg?branch=master\n   :target: https://coveralls.io/github/stdtom/ssl_certinfo?branch=master\n   :alt: Coveralls Test Coverage\n\n.. |codecov| image:: https://codecov.io/gh/stdtom/ssl_certinfo/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/stdtom/ssl_certinfo\n   :alt: CodeCov\n\n.. |codeclimate-cov| image:: https://api.codeclimate.com/v1/badges/1ed86e874b3c68672c5c/test_coverage\n   :target: https://codeclimate.com/github/stdtom/ssl_certinfo/test_coverage\n   :alt: Code Climate Test Coverage\n\n.. |pyup| image:: https://pyup.io/repos/github/stdtom/ssl_certinfo/shield.svg\n   :target: https://pyup.io/repos/github/stdtom/ssl_certinfo/\n   :alt: Updates\n\n.. |pyup-p3| image:: https://pyup.io/repos/github/stdtom/ssl_certinfo/python-3-shield.svg\n   :target: https://pyup.io/repos/github/stdtom/ssl_certinfo/\n   :alt: Python 3\n\n.. |requires| image:: https://requires.io/github/stdtom/ssl_certinfo/requirements.svg?branch=master\n   :target: https://requires.io/github/stdtom/ssl_certinfo/requirements/?branch=master\n   :alt: Requirements Status\n\n.. |version| image:: https://img.shields.io/pypi/v/ssl-certinfo.svg\n   :target: https://pypi.org/project/ssl-certinfo/\n   :alt: Version\n\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/ssl-certinfo.svg?logo=python&logoColor=FBE072\n    :target: https://pypi.org/project/ssl-certinfo/\n    :alt: Python versions supported\n\n.. |downloads| image:: https://pepy.tech/badge/ssl-certinfo\n    :target: https://pepy.tech/project/ssl-certinfo\n    :alt: PyPI downloads\n\n.. end-badges\n\n\nSSL CertInfo collects information about SSL certificates from a set of hosts.\n\n\nFeatures\n--------\n\n* Hosts to be scanned can be specified as a list of\n\n  * hostnames (fully qualified domain names), e.g. ``github.com``,\n  * ip addresses, e.g. ``1.1.1.1``,\n  * ip networks in CIDR format, e.g. ``10.0.0.0/24``,\n  * ip ranges, e.g. ``10.0.0.1-10.0.0.10``,\n  * or any combination of the previous.\n\n* Results will be presented in various output formats: ``--table``, ``--json``, ``--yaml``, ``--csv``, ``--raw``.\n\n\nInstallation\n------------\nYou can download and install the latest version of this software from the Python package index (PyPI) as follows::\n\n  $ pip install ssl_certinfo\n\n\nUsage\n-----\n\nWhen you install ssl_certinfo, a command-line script called ``ssl_certinfo`` is\nplaced on your path. You can invoke ssl_certinfo directly via this script from the command line::\n\n  $ ssl_certinfo [...]\n\n\nYou can also invoke it through the Python interpreter from the command line::\n\n  $ python -m ssl_certinfo [...]\n\n\nHelp is available with the ``--help`` or ``-h`` switch::\n\n  $ ssl_certinfo -h\n  usage: ssl_certinfo [-h] [-V] [-v | -q] [-p PORT] [-t TIMEOUT] [-T | -j | -y | -c | -r] [host [host ...]]\n\n  Collect information about SSL certificates from a set of hosts\n\n  positional arguments:\n  host                  Connect to HOST\n\n  optional arguments:\n  -h, --help            show this help message and exit\n  -V, --version         display version information and exit\n  -v, --verbose         verbose output (repeat for increased verbosity)\n  -q, --quiet           quiet output (show errors only)\n  -p PORT, --port PORT  TCP port to connnect to [0-65535]\n  -t TIMEOUT, --timeout TIMEOUT\n                        Maximum time allowed for connection\n  -T, --table           Print results in table format\n  -j, --json            Print results in JSON format\n  -y, --yaml            Print results in YAML format\n  -c, --csv             Print results in CSV format\n  -r, --raw             Print results in raw format\n\n\n\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `stdtom/cookiecutter-pypackage-pipenv`_ project template, based on `audreyr/cookiecutter-pypackage`_.\n\n.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter\n.. _`stdtom/cookiecutter-pypackage-pipenv`: https://github.com/stdtom/cookiecutter-pypackage-pipenv\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'StdTom',
    'author_email': 'stdtom@gmx.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stdtom/ssl_certinfo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
