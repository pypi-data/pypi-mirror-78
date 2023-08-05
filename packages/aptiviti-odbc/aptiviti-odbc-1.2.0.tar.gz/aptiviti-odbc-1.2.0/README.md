# aptiviti_odbc

[![Build Status](https://travis-ci.org/aptiviti/aptiviti-odbc.svg?branch=master)](https://travis-ci.org/aptiviti/aptiviti-odbc)

[![codecov](https://codecov.io/gh/aptiviti/aptiviti-odbc/branch/master/graph/badge.svg?token=UFVsUnyfTG)](https://codecov.io/gh/aptiviti/aptiviti-odbc)

Library to wrap helper functions for pyodbc in Aptiviti code. Target OS: Windows 10

## Install as module

`python3 -m pip install aptiviti-odbc`

Then you can

`from aptiviti_odbc import aptiviti_odbc_connection`

## Dependencies

First run

`python3 -m pip install requirements.txt`

before developing locally

## Build

Delete the `dist` folder if it already exists.
Don't forget to increment the version number in `setup.py `prior to building.
`python3 .\setup.py bdist_wheel` to create the `dist` folder containing the package build.

## Deploy to pypi

TravisCI is configured to automatically deploy to PyPi on pushed tag.

Increment the version number `setup.py`.
run `python3 -m twine upload .\dist\*` to upload to pypi. Currently this package is deployed to the `etrintel` pypi account.

You might run into the following error:

    HTTPError: 400 Client Error: File already exists. See https://pypi.org/help/#file-name-reuse for url: https://upload.pypi.org/legacy/

If that happens to you, check up on 2 things:

* Make sure you updated the version number in both files
* Delete the old version files from your dist/ directory