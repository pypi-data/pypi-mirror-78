#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import re

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []
with open('requirements.txt', 'r') as requirements_txt:
    for requirement in requirements_txt:
        requirement_match = re.findall('.*==.*(?= ;)|.*==.*',requirement)
        if requirement_match:
            requirements.append(requirement_match[0])

test_requirements = []
with open('requirements_dev.txt', 'r') as requirements_dev_txt:
    for requirement in requirements_dev_txt:
        requirement_match = re.findall('.*==.*(?= ;)|.*==.*',requirement)
        if requirement_match:
            test_requirements.append(requirement_match[0])

setup_requirements = []

setup(
    author="Darren Gruber",
    author_email='dgruber@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A CLI and Python Library for configuration AWS IAM authentication with MongoDB URI connection strings.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mongodb_iam_connection_string',
    name='mongodb_iam_connection_string',
    packages=find_packages(include=['mongodb_iam_connection_string', 'mongodb_iam_connection_string.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/darrengruber/mongodb-iam-connection-string',
    version='1.0.0',
    entry_points={"console_scripts": ["mics = mongodb_iam_connection_string.cli:cli"]},
    zip_safe=False,
)
