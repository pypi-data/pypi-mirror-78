# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ofx_processor', 'ofx_processor.processors', 'ofx_processor.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'dateparser>=0.7.6,<0.8.0',
 'ofxtools>=0.8.22,<0.9.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['ynab = ofx_processor.main:cli']}

setup_kwargs = {
    'name': 'ofx-processor',
    'version': '2.1.1',
    'description': 'Personal ofx processor',
    'long_description': '# ofx-processor\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ofx-processor)\n![PyPI - Format](https://img.shields.io/pypi/format/ofx-processor)\n![PyPI - Status](https://img.shields.io/pypi/status/ofx-processor)\n![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Crocmagnon/ofx-processor?include_prereleases)\n![License](https://img.shields.io/github/license/Crocmagnon/ofx-processor)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Crocmagnon/ofx-processor/Test%20&%20publish)\n![Sonar Coverage](https://img.shields.io/sonar/coverage/Crocmagnon_ofx-processor?server=https%3A%2F%2Fsonarcloud.io)\n[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Crocmagnon_ofx-processor&metric=bugs)](https://sonarcloud.io/dashboard?id=Crocmagnon_ofx-processor)\n[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Crocmagnon_ofx-processor&metric=code_smells)](https://sonarcloud.io/dashboard?id=Crocmagnon_ofx-processor)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Crocmagnon_ofx-processor&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=Crocmagnon_ofx-processor)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Crocmagnon_ofx-processor&metric=alert_status)](https://sonarcloud.io/dashboard?id=Crocmagnon_ofx-processor)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Crocmagnon_ofx-processor&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=Crocmagnon_ofx-processor)\n[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Crocmagnon_ofx-processor&metric=security_rating)](https://sonarcloud.io/dashboard?id=Crocmagnon_ofx-processor)\n[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=Crocmagnon_ofx-processor&metric=sqale_index)](https://sonarcloud.io/dashboard?id=Crocmagnon_ofx-processor)\n\n\n## Usage\n\n```shell script\nUsage: ynab [OPTIONS] COMMAND [ARGS]...\n\n  Import your data to YNAB with the processors listed below or manage your\n  config.\n\nOptions:\n  --version   Show the version and exit.\n  -h, --help  Show this message and exit.\n\nCommands:\n  config   Manage configuration.\n  bpvf     Import BPVF bank statement (OFX file).\n  ce       Import CE bank statement (OFX file).\n  lcl      Import LCL bank statement (OFX file).\n  revolut  Import Revolut bank statement (CSV file).\n```\n\nAll transactions will be pushed to YNAB. If this is your first time using the script,\nit will open a generated config file for you to fill up.\n\nThe account and budget UUID are found in the YNAB url when using the web app.\n\nThe file passed in parameter will be deleted unless specified (`--keep` option on each import command)\n\n## Versions\n\nThis project follows [Semantic Versioning](https://semver.org/). ',
    'author': 'Gabriel Augendre',
    'author_email': 'gabriel@augendre.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Crocmagnon/ofx-processor/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
