# rsyslog-postgres-viewer
[![Build Status](https://travis-ci.org/cope-systems/rsyslog-postgres-viewer.svg?branch=master)](https://travis-ci.org/cope-systems/rsyslog-postgres-viewer) 
[![Coverage Status](https://coveralls.io/repos/github/cope-systems/rsyslog-postgres-viewer/badge.svg?branch=master)](https://coveralls.io/github/cope-systems/rsyslog-postgres-viewer?branch=master)
[![PyPI version](https://badge.fury.io/py/rsyslog-postgres-tools.svg)](https://badge.fury.io/py/rsylog-postgres-tools)

## About

A simple application for viewing rsyslog logs stored in PostgreSQL. 
**rsyslog-postgres-tools** leverages Python with the Bottle web framework
and eventlet to provide an HTTP viewer and OpenAPI 2.0 REST API.

## Installation

* The repository may either be installed locally using setup.py
  (```python setup.py install```) or may be built as a docker container,
  and executed through docker. See the provided Makefile for building a 
  tagged container.


## Usage

* The primary entrypoint for rsyslog-postgres-tools is the ```run_rp_tools.py```
  script. Available commands are as follows:
  * **bootstrap**: Bootstrap the PostgreSQL database schema for the target database, 
    so that rsyslog may be used with the ompgsql module to begin logging events.
  * **clean**: Remove system events older that a given time back. This is used to ensure
    the database does not continue to grow indefinitely, and should be set to run as 
    a cron job (or similar).
  * **run_http_server**: Start a web server for viewing and searching the system event logs. 
    This web server also provides an OpenAPI 2.0 Swagger API for programmatic
    log searching and retrieval.
  * **search**: Run a search on the target database for events matching the 
    specified parameters. Matching events are printed to stdout in a
    user configurable format.
  * **tail**: Begin tailing the target database, and printing new
    system events as they are inserted. This functions similar to
    how ```tail -f``` works on regular files. The output format, like
    **search** is user configurable.
    
  For more information on each command, the user may make use of the
  help parameter (```-h```) when invoking the ```run_rp_tools.py``` script.


## Contributing

Contributions are encouraged, and may be made via pull requests to the [rsyslog-postgres-viewer 
Github repository](https://github.com/cope-systems/rsyslog-postgres-viewer). Unit tests are expected for any
additional changes or improvements made to the codebase, and all tests must pass for a 
pull request to be considered for merging. Please note that this
codebase is licensed as AGPL v3, and contributions will be required to conform to
this license.

## Changelog

### Version 0.1.0

* Initial open sourcing of this codebase. Tools include a command line syslog tailing mechanism, 
  a command line search tool, a command line database event purging tool,
  and an web based syslog viewer.