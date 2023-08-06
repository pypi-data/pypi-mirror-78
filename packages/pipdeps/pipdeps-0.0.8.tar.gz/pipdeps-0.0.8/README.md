# pipdeps

Pipdeps shows/upgrades outdated packages with respect to existing dependencies.

Python 2.7 is required.

In principle, resolving dependencies and requirements of all packages and
their versions is easy. Unfortunately, computing resources of standard
computer may not be sufficient even for little group of packages/versions.
In an effort to decrease number of possibilities, we make some attempts to
solve partial tasks. On the other hands, it may lead to some unwanted
situations. Currently, package extras are not finished.

## Usage

```console
$ pipdeps --help
usage: pipdeps [-h] [-e [EXCLUDE [EXCLUDE ...]]]
               (-l | -t | -u | -s [SHOW [SHOW ...]])

Pipdeps shows/upgrades outdated packages with respect to existing
dependencies.

optional arguments:
  -h, --help            show this help message and exit
  -e [EXCLUDE [EXCLUDE ...]], --exclude [EXCLUDE [EXCLUDE ...]]
                        Space-separated list of excluded package (and
                        version). Format package==version or package for all
                        versions
  -l, --list            show list of upgradeable packages and versions
  -t, --table           show table of upgradeable packages and versions
  -u, --upgrade         upgrade upgradeable packages
  -s [SHOW [SHOW ...]], --show [SHOW [SHOW ...]]
                        show detailed info about upgradeable packages
```

## Changelog


## 0.0.8 (2020-09-02)

### Other

* Fix requires-python. [Marek Chrastina]


## 0.0.7 (2020-08-28)

### Other

* Fix platform_system. [Marek Chrastina]

* Update CI. [Marek Chrastina]


## 0.0.6 (2020-03-25)

### Other

* Add python safety to CI. [Marek Chrastina]

* Add exclude argument. [Marek Chrastina]

* There is show list and show table arguments now. [Marek Chrastina]

* Update pyenv pip setuptools in CI. [Marek Chrastina]

* If only bdist is available, check if python_version satisfied python platform version. [Marek Chrastina]


## 0.0.5 (2019-10-21)

### Other

* Fix showing 0.0.0 version. [Marek Chrastina]


## 0.0.4 (2019-10-21)

### Other

* Serious bugs in pipdeptree, do not use it anymore. [Marek Chrastina]

* Requires.txt is not mandatory for metadata generator. [Marek Chrastina]


## 0.0.3 (2019-08-29)

### Other

* Case vanished module; all deps are taken from metadata; hotfix extras. [Marek Chrastina]


## 0.0.2 (2019-08-16)

### Other

* Remove version.py. [Marek Chrastina]

* Add history. [Marek Chrastina]


## 0.0.1 (2019-08-16)

### Other

* Add documentation to CI. [Marek Chrastina]

* Add install test, version check and deploy to CI. [Marek Chrastina]

* Add pycodestyle to CI. [Marek Chrastina]

* Add show option. [Marek Chrastina]

* Requires of possible upgradable package versions has to be taken into account. [Marek Chrastina]

* Collect data for all packages. [Marek Chrastina]

* Upgrade pip first. [Marek Chrastina]

* Check for python version. [Marek Chrastina]

* Tabulate print list. [Marek Chrastina]

* Add list option. [Marek Chrastina]

* Code refactoring. [Marek Chrastina]

* Make pylint happy. [Marek Chrastina]

* Add build ci. [Marek Chrastina]

* Add setup.py and __init__.py. [Marek Chrastina]

* Add py script. [Marek Chrastina]

* Add LICENSE. [Marek Chrastina]

* Add README. [Marek Chrastina]


