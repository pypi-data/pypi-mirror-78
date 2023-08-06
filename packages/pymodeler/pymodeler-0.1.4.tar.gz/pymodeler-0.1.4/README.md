PyModeler
---------

[![Build](https://img.shields.io/travis/kadrlica/pymodeler.svg)](https://travis-ci.org/kadrlica/pymodeler)
[![Release](https://img.shields.io/github/release/kadrlica/pymodeler.svg)](../../releases)
[![PyPI](https://img.shields.io/pypi/v/pymodeler.svg)](https://pypi.python.org/pypi/pymodeler)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/kadrlica/pymodeler)

Description
-----------

This is a small (and hopefully generic) package for dealing with predictive models and their parameters in python. A Model is a storage container allowing easy access to a set of Parameters. Parameters are mutable numbers and associated bounding ranges, estimated errors, and fit freedom.

Installation
------------
The easiest way is using `pip`. To get the latest release

```
# for the first install
pip install pymodeler

# update just pymodeler
pip install pymodeler --no-deps --upgrade --ignore-installed

# update pymodeler and all dependencies
pip install pymodeler --upgrade
```

You can also get the latest release or version of the soure code from github...

```
git clone https://github.com/kadrlica/pymodeler.git
cd pymodeler
python setup.py install
```
