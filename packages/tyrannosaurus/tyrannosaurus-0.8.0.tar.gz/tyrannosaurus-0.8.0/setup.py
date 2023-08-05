# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyrannosaurus']

package_data = \
{'': ['*'], 'tyrannosaurus': ['resources/*']}

install_requires = \
['grayskull>=0.8.1,<1.0',
 'requests>=2,<3',
 'tomlkit>=0.5,<1.0',
 'typer>=0.3,<1.0']

entry_points = \
{'console_scripts': ['tyrannosaurus = tyrannosaurus.cli:cli']}

setup_kwargs = {
    'name': 'tyrannosaurus',
    'version': '0.8.0',
    'description': 'Opinionated Python template and metadata synchronizer for 2020.',
    'long_description': '# Tyrannosaurus Reqs\n[![Version status](https://img.shields.io/pypi/status/tyrannosaurus)](https://pypi.org/project/tyrannosaurus/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tyrannosaurus)](https://pypi.org/project/tyrannosaurus/)\n[![Docker](https://img.shields.io/docker/v/dmyersturnbull/tyrannosaurus?color=green&label=DockerHub)](https://hub.docker.com/repository/docker/dmyersturnbull/tyrannosaurus)\n[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/dmyersturnbull/tyrannosaurus?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/tyrannosaurus/releases)\n[![Latest version on PyPi](https://badge.fury.io/py/tyrannosaurus.svg)](https://pypi.org/project/tyrannosaurus/)\n[![Documentation status](https://readthedocs.org/projects/tyrannosaurus/badge/?version=latest&style=flat-square)](https://tyrannosaurus.readthedocs.io/en/stable/)\n[![Build & test](https://github.com/dmyersturnbull/tyrannosaurus/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/tyrannosaurus/actions)\n[![Travis](https://img.shields.io/travis/dmyersturnbull/tyrannosaurus?label=Travis)](https://travis-ci.org/dmyersturnbull/tyrannosaurus)\n[![Azure DevOps builds](https://img.shields.io/azure-devops/build/dmyersturnbull/0350c934-2512-4592-848e-9db46c63241a/1?label=Azure)](https://dev.azure.com/dmyersturnbull/tyrannosaurus/_build?definitionId=1&_a=summary)\n[![Maintainability](https://api.codeclimate.com/v1/badges/5e3b38c9b9c418461dc3/maintainability)](https://codeclimate.com/github/dmyersturnbull/tyrannosaurus/maintainability)\n[![Coverage](https://coveralls.io/repos/github/dmyersturnbull/tyrannosaurus/badge.svg?branch=master)](https://coveralls.io/github/dmyersturnbull/tyrannosaurus?branch=master)\n\nAn opinionated, forwards-looking Python template for 2020.\nNo setup.py, requirements.txt, or eggs.\n\nI wrote this after making nearly 50 commits to configure\nreadthedocs, PyPi, Tox, Docker, Travis, and Github actions.\nThis avoids that struggle for 99% of projects.\nJust clone and modify or use `tyrannosaurus new`.\nInstall with `pip install tyrannosaurus`.\n\n- _When you commit_, your code is linted.\n- _When you push or make a pull request_, your code is built and tested.\n  Security checks are run, style is checked,\n  documentation is generated, and docker images, sdists, and wheels are built.\n- _When you release on Github_, your code is published to PyPi and DockerHub.\n  Just add `PYPI_TOKEN` and `COVERALLS_REPO_TOKEN` as Github repo secrets.\n\nIf you’re curious why older infrastructure (setup.py, etc) is problematic,\nsee [this post](https://dmyersturnbull.github.io/#-the-python-build-landscape).\n\n⚠ Status: Alpha. Generally works well, but\n   the `sync` command does less than advertised.\n\n##### Integrations:\n\nAlso comes with nice Github labels, issue templates, a changelog template,\nTravis support, Conda recipe and environment generation, and other integrations.\nTyrannosaurus itself is included as a dependency.\nRunning `tyrannosaurus build` will run poetry lock, synchronize project metadata, build, run tests, install,\nand clean up. The project metadata is synchronized from `pyproject.toml` to other files,\nsuch as Anaconda recipes and environment files, license headers, doc and tox requirements, and author/contributor lists.\nTarget files can be disabled in `[tool.tyrannosaurus.targets]`.\n\n\n##### To build your own code:\n\nTo run locally, install [Poetry](https://github.com/python-poetry/poetry)\nand [Tox](https://tox.readthedocs.io/en/latest/) (`pip install tox`).\nThen just type `tox` to build artifacts and run tests.\nTo create an initial Anaconda recipe or environment file, run `tyrannosaurus recipe` or `tyrannosaurus env`.\n\n**[See the docs](https://tyrannosaurus.readthedocs.io/en/stable/)** for more information.\n\n##### Contributing:\n\n[New issues](https://github.com/dmyersturnbull/tyrannosaurus/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/tyrannosaurus/blob/master/CONTRIBUTING.md).\nGenerated with tyrannosaurus: `tyrannosaurus new tyrannosaurus`\n\n\n```text\n                                              .++++++++++++.\n                                           .++HHHHHHH^^HHH+.\n                                          .HHHHHHHHHH++-+-++.\n                                         .HHHHHHHHHHH:t~~~~~\n                                        .+HHHHHHHHHHjjjjjjjj.\n                                       .+NNNNNNNNN/++/:--..\n                              ........+NNNNNNNNNN.\n                          .++++BBBBBBBBBBBBBBB.\n .tttttttt:..           .++BBBBBBBBBBBBBBBBBBB.\n+tt+.      ``         .+BBBBBBBBBBBBBBBBBBBBB+++cccc.\nttt.               .-++BBBBBBBBBBBBBBBBBBBBBB++.ccc.\n+ttt++++:::::++++++BBBBBBBBBBBBBBBBBBBBBBB+..++.\n.+TTTTTTTTTTTTTBBBBBBBBBBBBBBBBBBBBBBBBB+.    .ccc.\n  .++TTTTTTTTTTBBBBBBBBBBBBBBBBBBBBBBBB+.      .cc.\n    ..:++++++++++++++++++BBBBBB++++BBBB.\n           .......      -LLLLL+. -LLLLL.\n                        -LLLL+.   -LLLL+.\n                        +LLL+       +LLL+\n                        +LL+         +ff+\n                        +ff++         +++:\n                        ++++:\n```\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/tyrannosaurus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
