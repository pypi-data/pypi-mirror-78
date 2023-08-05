#!/usr/bin/env python3
# Encoding: UTF-8
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 0):
    raise RuntimeError('Elsa needs Python 3 or greater')


def long_description():
    with open('README.rst') as readme:
        ld = readme.read()
    ld += '\n\n'
    with open('CHANGELOG.rst') as changelog:
        ld += changelog.read()
    return ld


setup(
    name='elsa',
    version='0.1.6',
    description='Helper module for Frozen-Flask based websites',
    long_description=long_description(),
    keywords='flask web github',
    author='Miro Hrončok',
    author_email='miro@hroncok.cz',
    license='MIT',
    url='https://github.com/pyvec/elsa',
    packages=[p for p in find_packages() if p != 'tests'],
    install_requires=[
        'click',
        'Flask',
        'Frozen-Flask >= 0.15',
        'ghp-import',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3', 'requests', 'pytest-flake8'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
