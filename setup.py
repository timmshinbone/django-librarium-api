"""Sets up the package"""

#!/usr/bin/env python
 # -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE.md') as f:
    LICENSE = f.read()

setup(
    name='django-librarium',
    version='0.1.0',
    description='Django version of Flask app Librarium',
    long_description=README,
    author='Timm Schoenborn',
    author_email='timmschoenborn@gmail.com',
    url='https://github.com/timmshinbone/django-librarium-api',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
