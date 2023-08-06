#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split()

setup(
    name='minnie-config',
    version='0.1.0',
    description='Datajoint configurations for the microns_minnie65_* phase 3 schemas.',
    author='Christos Papadopoulos',
    author_email='cpapadop@bcm.edu',
    packages=find_packages(exclude=[]),
    install_requires=requirements,
    entry_points = {
        'console_scripts': [
            'minnie-config = minnie_config.cli:mounter'
        ]
    }
)
