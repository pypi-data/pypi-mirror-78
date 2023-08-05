# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mergecounts', 'mergecounts.utils']

package_data = \
{'': ['*']}

install_requires = \
['dxpy>=0.298.1,<0.299.0',
 'hurry.filesize>=0.9,<0.10',
 'logzero>=1.5.0,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'requests<2.24.0',
 'tables>=3.6.1,<4.0.0',
 'tqdm>=4.48.2,<5.0.0']

entry_points = \
{'console_scripts': ['stjudecloud-merge-counts = mergecounts.__main__:run']}

setup_kwargs = {
    'name': 'stjudecloud-merge-counts',
    'version': '1.1.0',
    'description': 'Utility for merging RNA-seq expression counts files from St. Jude Cloud.',
    'long_description': '<p align="center">\n  <h1 align="center">\n    merge-counts\n  </h1>\n\n  <p align="center">\n    <a href="https://actions-badge.atrox.dev/stjudecloud/merge-counts/goto" target="_blank">\n      <img alt="Actions: CI Status"\n          src="https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fstjudecloud%2Fmerge-counts%2Fbadge&style=flat" />\n    </a>\n    <a href="https://pypi.org/project/merge-counts/" target="_blank">\n      <img alt="PyPI"\n          src="https://img.shields.io/pypi/v/merge-counts?color=orange">\n    </a>\n    <a href="https://pypi.python.org/pypi/merge-counts/" target="_blank">\n      <img alt="PyPI: Downloads"\n          src="https://img.shields.io/pypi/dm/merge-counts?color=orange">\n    </a>\n    <a href="https://pypi.python.org/pypi/merge-counts/" target="_blank">\n      <img alt="PyPI: Downloads"\n          src="https://img.shields.io/pypi/pyversions/merge-counts?color=orange">\n    </a>\n    <a href="https://github.com/stjudecloud/merge-counts/blob/master/LICENSE.md" target="_blank">\n    <img alt="License: MIT"\n          src="https://img.shields.io/badge/License-MIT-blue.svg" />\n    </a>\n  </p>\n\n\n  <p align="center">\n    Utility for merging RNA-seq expression counts files from St. Jude Cloud. \n    <br />\n    <br />\n    <a href="https://github.com/stjudecloud/merge-counts/issues/new?assignees=&labels=&template=feature_request.md&title=Descriptive%20Title&labels=enhancement">Request Feature</a>\n    ·\n    <a href="https://github.com/stjudecloud/merge-counts/issues/new?assignees=&labels=&template=bug_report.md&title=Descriptive%20Title&labels=bug">Report Bug</a>\n    ·\n    ⭐ Consider starring the repo! ⭐\n    <br />\n  </p>\n</p>\n\n## 📚 Getting Started\n\n### Installation\n\nYou can install merge-counts using the Python Package Index ([PyPI](https://pypi.org/)).\n\n```bash\npip install merge-counts\n```\n\n## 🖥️ Development\n\nIf you are interested in contributing to the code, please first review\nour [CONTRIBUTING.md][contributing-md] document. \n\nTo bootstrap a development environment, please use the following commands.\n\n```bash\n# Clone the repository\ngit clone git@github.com:stjudecloud/merge-counts.git\ncd merge-counts\n\n# Install the project using poetry\npoetry install\n```\n\n## 🚧️ Tests\n\nmerge-counts provides a (currently patchy) set of tests — both unit and end-to-end.\n\n```bash\npy.test\n```\n\n## 🤝 Contributing\n\nContributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/stjudecloud/merge-counts/issues). You can also take a look at the [contributing guide][contributing-md].\n\n## 📝 License\n\nThis project is licensed under the MIT License—see the [LICENSE.md][license-md] file for details.\n\nCopyright © 2020 [St. Jude Cloud Team](https://github.com/stjudecloud).<br />\n\n[contributing-md]: https://github.com/stjudecloud/merge-counts/blob/master/CONTRIBUTING.md\n[license-md]: https://github.com/stjudecloud/merge-counts/blob/master/LICENSE.md\n',
    'author': 'Clay McLeod',
    'author_email': 'Clay.McLeod@STJUDE.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stjudecloud/merge-counts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
