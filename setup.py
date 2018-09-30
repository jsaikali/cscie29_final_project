#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', 'setuptools_scm']

test_requirements = ['pytest', ]

setup(
    author="Joanna Saikali",
    author_email='joanna.saikali@gmail.com',
    use_scm_version = True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Adapted Python Boilerplate for use in the CSCI-E-29 course.",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pset_02',
    name='pset_02',
    packages=find_packages(include=['pset_02']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/csci-e-29/pset_2-jsaikali.git',
    version='0.1.0',
    zip_safe=False,
)
