# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tribool',
    version='0.0.1',
    description='Tribool data type',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks..com',
    url='https://github.com/grantjenks/tribool',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
