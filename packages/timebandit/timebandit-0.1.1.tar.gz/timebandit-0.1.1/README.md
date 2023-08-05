# Time Bandit

![header_image](header_image.jpg)

[![netlify badge](https://api.netlify.com/api/v1/badges/416b8ca3-82db-470f-9adf-a6d06264ca75/deploy-status)](https://app.netlify.com/sites/mystifying-keller-ab5658/deploys) [![Build Status](https://travis-ci.com/skeptycal/.dotfiles.svg?branch=dev)](https://travis-ci.com/skeptycal/.dotfiles)

## Timer utilities for Python 3.5+ Development

[![macOS Version](https://img.shields.io/badge/macOS-10.16%20BigSur-blue?logo=apple)](https://www.apple.com) [![GitHub Pipenv locked Python version](https://img.shields.io/badge/Python-3.9-yellow?color=3776AB&logo=python&logoColor=yellow)](https://www.python.org/) [![nuxt.js](https://img.shields.io/badge/nuxt.js-2.14.0-35495e?logo=nuxt.js)](https://nuxtjs.org/)

These are handy automation and informational utilities. Add more, change some, make some additions/corrections...

**Please feel free to offer suggestions and [changes][repo-issues]**.

> Copyright © 1976-2020 [Michael Treanor](https:/skeptycal.github.com)

[![License](https://img.shields.io/badge/License-MIT-darkblue)][skep-mit]

## Installation

### TLDR: clone the repo and run `./setup.sh`

## WHY?

-   comparison of different methods
-   profiling features under real world loads with decorators and log readers
-   visualize outcomes in unique ways

---

[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/3454/badge)](https://bestpractices.coreinfrastructure.org/projects/3454) [![test coverage](https://img.shields.io/badge/test_coverage-100%25-6600CC.svg?logo=Coveralls&color=3F5767)](https://coveralls.io)

---

## Prerequisites

-   Python version 3.5+

### Recommended IDE setup:

-   [VSCode][get-code] IDE
-   [Sarah Drasner][sdras]'s Vue VSCode [Extension Pack][sdras-pack]
-   [Don Jayamanne][djay]'s Python [Extension Pack][djay-pack]

### Installed by this setup as needed:

-   [Homebrew][brew]
-   GNU [coreutils][coreutils] for macOS (brew install coreutils)
-   [Pre-Commit][pre-commit] for automated checks
-   [Poetry][poetry] for dependency management, building, publishing, and versioning

## Install

    pip install timebandit

    - or -

if you wish to make modifications or contribute to the open source project:

```sh
# clone the repo
git clone https://www.github.com/skeptycal/

# change to the repo directory
cd user_bin_dir_repo

# run the init script
./init

# optional: # use './init --nobrew' to skip install of homebrew and utilities
./init --nobrew
```

---

## Usage

```py
from timebandit import timeit

# as a decorator

@timeit
def myfunction(x):
    ... do stuff ...

#     - or -

# as a function call

the_result = timeit(myfunction(5))
print(the_result)
```

---

## Feedback

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

Suggestions/improvements are [welcome][repo-issues]!

---

## Author

[![twitter/skeptycal](https://s.gravatar.com/avatar/b939916e40df04f870b03e0b5cff4807?s=80)](http://twitter.com/skeptycal 'Follow @skeptycal on Twitter')

[**Michael Treanor**][me]

![Twitter Follow](https://img.shields.io/twitter/follow/skeptycal.svg?style=social) ![GitHub followers](https://img.shields.io/github/followers/skeptycal.svg?label=GitHub&style=social)

[repo-issues]: (https://github.com/skeptycal/dotfiles/issues)
[repo-fork]: (https://github.com/skeptycal/dotfiles/fork)
[me]: (https://www.skeptycal.com)
[skep-image]: (https://s.gravatar.com/avatar/b939916e40df04f870b03e0b5cff4807?s=80)
[skep-twitter]: (http://twitter.com/skeptycal)
[skep-mit]: (https://skeptycal.mit-license.org/1976/)
[mb]: (https://mathiasbynens.be/)
[sdras]: (https://sarahdrasnerdesign.com/)
[djay]: (https://github.com/DonJayamanne)
[get-code]: (https://code.visualstudio.com/download)
[brew]: (https://brew.sh/)
[djay-pack]: (https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)
[sdras-pack]: (https://marketplace.visualstudio.com/items?itemName=sdras.vue-vscode-extensionpack)
[pre-commit]: (https://pre-commit.com/)
[xcode]: (https://developer.apple.com/xcode/)
[coreutils]: (https://www.gnu.org/software/coreutils/)
[poetry]: (https://python-poetry.org/)
