#!/usr/bin/env python
import os
from setuptools import setup


def _read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


REQUIREMENTS = [l for l in _read('requirements.txt').split('\n') if l and not l.startswith('#')]
DEV_REQUIREMENTS = REQUIREMENTS + [
    l for l in _read('requirements.txt').split('\n')
    if l and not l.startswith('#') and not l.startswith("-r")
]
VERSION = _read("VERSION")


setup(
    name='rsyslog-postgres-tools',
    version=VERSION,
    url='https://github.com/cope-systems/rsyslog-postgres-viewer',
    description='Tools for using PostgreSQL as the storage medium for rsyslog logging.',
    # long_description=_read("README.md"),
    author='Robert Cope',
    author_email='robert@copesystems.com',
    license='AGPL v3',
    platforms='any',
    packages=["rsyslog_postgres_tools"],
    scripts=["run_rp_tools.py"],
    install_requires=REQUIREMENTS,
    tests_require=DEV_REQUIREMENTS,
    classifiers=[
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: SQL',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database',
        'Topic :: Internet :: Log Analysis',
        'Topic :: System :: Logging',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Development Status :: 4 - Beta'
    ],
    include_package_data=True,
    keywords="postgresql postgres syslog rsyslog logging sysadmin systems administration"
)
