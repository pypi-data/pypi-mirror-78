# Campbell Scientific CR6 WiFi Python Client

[![pipeline status](https://gitlab.com/tue-umphy/instruments/python3-csiweb/badges/master/pipeline.svg)](https://gitlab.com/tue-umphy/instruments/python3-csiweb/commits/master)
[![coverage report](https://gitlab.com/tue-umphy/instruments/python3-csiweb/badges/master/coverage.svg)](https://tue-umphy.gitlab.io/instruments/python3-csiweb/coverage-report/)
[![documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)](https://tue-umphy.gitlab.io/instruments/python3-csiweb)
[![PyPI](https://badge.fury.io/py/csiweb.svg)](https://badge.fury.io/py/csiweb)

`csiweb` is a Python package to interface a Campbell Scientific data logger via
its CSI web server interface.

## Installation

First, make sure you have a recent version of `setuptools`:

```bash
python3 -m pip install --user --upgrade setuptools
```

Then, to install, run from the repository root:

```bash
python3 -m pip install --user .
```

or install it from [PyPi](https://pypi.org/project/csiweb):

```bash
python3 -m pip install --user csiweb
```

(Run `sudo apt-get update && sudo apt-get -y install python3-pip` if it
complains about `pip` not being found)

## What can `csiweb` do?

- periodically query data from a CSI web server
- publish the data via MQTT to one or more configurable brokers
- a systemd user service file is also provided

## Documentation

Documentation of the `csiweb` package can be found [here on
GitLab](https://tue-umphy.gitlab.io/instruments/python3-csiweb/).

Also, the command-line help page `csiweb -h` is your friend.
