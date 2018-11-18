#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import subprocess

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.test import test

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'

with open('README.rst', 'r') as readme_file:
    readme = readme_file.read()


def get_version(*file_paths):
    """Retrieves the version from project/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        subprocess.check_call(['pipenv', 'install', '--dev', '--deploy', '--system'])
        develop.run(self)


class TestCommand(test):
    """Run tests"""

    def run(self):
        subprocess.check_call(['pytest'])
        test.run(self)


setup(
    name='dotty_dict',
    version=get_version('dotty_dict', '__init__.py'),
    description="Dictionary wrapper for quick access to deeply nested keys.",
    long_description=readme,
    license="MIT license",
    author="Paweł Zadrożny @pawelzny",
    author_email='pawel.zny@gmail.com',
    url='https://github.com/pawelzny/dotty_dict',
    packages=find_packages(exclude=('tests', 'docs', 'bin', 'example')),
    package_dir={'dotty_dict': 'dotty_dict'},
    include_package_data=True,
    use_scm_version=True,
    install_requires=['setuptools_scm'],
    zip_safe=False,
    keywords='dot notation dict wrapper helper utils lib',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'test': TestCommand,
    },
)
