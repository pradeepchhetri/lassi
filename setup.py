#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

packages = [
    'lassi',
    'lassi.lib'
]

requires = open("requirements/base.txt").read().split()

setup(
    name='lassi',
    version='0.0.1',
    description='Basic Configuration Management Tool',
    packages=find_packages(),
    package_dir={'lassi': 'lassi'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'lassi = lassi.lassi:main'
        ]
    },
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
    )
)
