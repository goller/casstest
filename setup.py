#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'cassandra-driver==2.1.3'
]

test_requirements = [
    'tox==1.8.1'
]

setup(
    name='casstest',
    version='0.3.0',
    description='Just a quick dockerfile test for my entertainment',
    long_description=readme + '\n\n' + history,
    author='Chris Goller',
    author_email='goller@gmail.com',
    url='https://github.com/goller/casstest',
    packages=[
        'casstest',
    ],
    package_dir={'casstest':
                 'casstest'},
    entry_points={'console_scripts': ['run-cass-test = casstest.casstest:main']},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='casstest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
