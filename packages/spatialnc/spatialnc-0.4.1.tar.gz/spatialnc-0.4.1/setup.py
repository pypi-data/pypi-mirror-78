#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = ['pytest', ]

setup(
    author="USDA ARS NWRC",
    author_email='snow@ars.usda.gov',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python library for handling spatial data in netcdfs specifically for modeling with SMRF/AWSM",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'nc_stats=spatialnc.cli:nc_stats',
            'make_projected_nc=spatialnc.cli:make_projected_nc']},
    keywords='spatialnc',
    name='spatialnc',
    packages=find_packages(include=['spatialnc']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/USDA-ARS-NWRC/spatialnc',
    zip_safe=False,
    use_scm_version={
        'local_scheme': 'node-and-date',
    },
    setup_requires=[
        'setuptools_scm',
        'pytest-runner'
    ],
)
