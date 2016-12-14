#!/usr/bin/env python

import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

REQUIREMENTS = [
    'argparse >= 1.4.0',
    'requests >= 2.5.1'
]

REQUIREMENTS_TEST = [
    'coverage',
    'nose',
    'mock >= 1.0.1',
    'tox'
]

KEYWORDS = [
    'deployment',
    'tickets'
]

setup(
    name='deploy-tix',
    version='0.0.5',
    description='Python scripts for creating services deployment tickets',
    author='Richard Pappalardo',
    author_email='rpappalax@gmail.com',
    url='https://github.com/rpappalax/deploy-tix',
    license="MIT",
    tests_require=REQUIREMENTS_TEST,
    install_requires=REQUIREMENTS,
    keywords=KEYWORDS,
    packages=['deploy_tix'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'ticket = deploy_tix.__main__:main'
        ]
    }
)
