# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timebandit']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0', 'wheel>=0.35.1,<0.36.0']

setup_kwargs = {
    'name': 'timebandit',
    'version': '0.1.1',
    'description': 'The most fabulous time measuring object in the world.',
    'long_description': "# Time Bandit\n\n![header_image](header_image.jpg)\n\n[![netlify badge](https://api.netlify.com/api/v1/badges/416b8ca3-82db-470f-9adf-a6d06264ca75/deploy-status)](https://app.netlify.com/sites/mystifying-keller-ab5658/deploys) [![Build Status](https://travis-ci.com/skeptycal/.dotfiles.svg?branch=dev)](https://travis-ci.com/skeptycal/.dotfiles)\n\n## Timer utilities for Python 3.5+ Development\n\n[![macOS Version](https://img.shields.io/badge/macOS-10.16%20BigSur-blue?logo=apple)](https://www.apple.com) [![GitHub Pipenv locked Python version](https://img.shields.io/badge/Python-3.9-yellow?color=3776AB&logo=python&logoColor=yellow)](https://www.python.org/) [![nuxt.js](https://img.shields.io/badge/nuxt.js-2.14.0-35495e?logo=nuxt.js)](https://nuxtjs.org/)\n\nThese are handy automation and informational utilities. Add more, change some, make some additions/corrections...\n\n**Please feel free to offer suggestions and [changes][repo-issues]**.\n\n> Copyright © 1976-2020 [Michael Treanor](https:/skeptycal.github.com)\n\n[![License](https://img.shields.io/badge/License-MIT-darkblue)][skep-mit]\n\n## Installation\n\n### TLDR: clone the repo and run `./setup.sh`\n\n## WHY?\n\n-   comparison of different methods\n-   profiling features under real world loads with decorators and log readers\n-   visualize outcomes in unique ways\n\n---\n\n[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/3454/badge)](https://bestpractices.coreinfrastructure.org/projects/3454) [![test coverage](https://img.shields.io/badge/test_coverage-100%25-6600CC.svg?logo=Coveralls&color=3F5767)](https://coveralls.io)\n\n---\n\n## Prerequisites\n\n-   Python version 3.5+\n\n### Recommended IDE setup:\n\n-   [VSCode][get-code] IDE\n-   [Sarah Drasner][sdras]'s Vue VSCode [Extension Pack][sdras-pack]\n-   [Don Jayamanne][djay]'s Python [Extension Pack][djay-pack]\n\n### Installed by this setup as needed:\n\n-   [Homebrew][brew]\n-   GNU [coreutils][coreutils] for macOS (brew install coreutils)\n-   [Pre-Commit][pre-commit] for automated checks\n-   [Poetry][poetry] for dependency management, building, publishing, and versioning\n\n## Install\n\n    pip install timebandit\n\n    - or -\n\nif you wish to make modifications or contribute to the open source project:\n\n```sh\n# clone the repo\ngit clone https://www.github.com/skeptycal/\n\n# change to the repo directory\ncd user_bin_dir_repo\n\n# run the init script\n./init\n\n# optional: # use './init --nobrew' to skip install of homebrew and utilities\n./init --nobrew\n```\n\n---\n\n## Usage\n\n```py\nfrom timebandit import timeit\n\n# as a decorator\n\n@timeit\ndef myfunction(x):\n    ... do stuff ...\n\n#     - or -\n\n# as a function call\n\nthe_result = timeit(myfunction(5))\nprint(the_result)\n```\n\n---\n\n## Feedback\n\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)\n\nSuggestions/improvements are [welcome][repo-issues]!\n\n---\n\n## Author\n\n[![twitter/skeptycal](https://s.gravatar.com/avatar/b939916e40df04f870b03e0b5cff4807?s=80)](http://twitter.com/skeptycal 'Follow @skeptycal on Twitter')\n\n[**Michael Treanor**][me]\n\n![Twitter Follow](https://img.shields.io/twitter/follow/skeptycal.svg?style=social) ![GitHub followers](https://img.shields.io/github/followers/skeptycal.svg?label=GitHub&style=social)\n\n[repo-issues]: (https://github.com/skeptycal/dotfiles/issues)\n[repo-fork]: (https://github.com/skeptycal/dotfiles/fork)\n[me]: (https://www.skeptycal.com)\n[skep-image]: (https://s.gravatar.com/avatar/b939916e40df04f870b03e0b5cff4807?s=80)\n[skep-twitter]: (http://twitter.com/skeptycal)\n[skep-mit]: (https://skeptycal.mit-license.org/1976/)\n[mb]: (https://mathiasbynens.be/)\n[sdras]: (https://sarahdrasnerdesign.com/)\n[djay]: (https://github.com/DonJayamanne)\n[get-code]: (https://code.visualstudio.com/download)\n[brew]: (https://brew.sh/)\n[djay-pack]: (https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)\n[sdras-pack]: (https://marketplace.visualstudio.com/items?itemName=sdras.vue-vscode-extensionpack)\n[pre-commit]: (https://pre-commit.com/)\n[xcode]: (https://developer.apple.com/xcode/)\n[coreutils]: (https://www.gnu.org/software/coreutils/)\n[poetry]: (https://python-poetry.org/)\n",
    'author': 'skeptycal',
    'author_email': 'skeptycal@gmail.com',
    'maintainer': 'skeptycal',
    'maintainer_email': 'skeptycal@gmail.com ',
    'url': 'https://skeptycal.github.io/timebandit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
