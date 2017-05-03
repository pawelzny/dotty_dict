#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []
test_requirements = [
    'coverage==4.3.4',
    'mock>=1.0.1',
    'flake8==3.3.0',
    'tox==2.7.0',
    'codecov>=2.0.0',
]

setup(
    name='dotty_dict',
    version='0.1.7',
    description="Dotty dict-like object allow to access deeply nested keys using dot notation.",
    long_description=readme + '\n\n' + history,
    author="Paweł Zadrożny",
    author_email='pawel.zny@gmail.com',
    url='https://github.com/pawelzny/dotty_dict',
    packages=[
        'dotty_dict',
    ],
    package_dir={'dotty_dict': 'dotty_dict'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='dotty_dict',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
