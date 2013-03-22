# -*- coding: utf-8 -*-

import os
import sys

import tribool

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tribool',
    version=tribool.__version__,
    description='Tribool data type',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='https://github.com/grantjenks/tribool',
    py_modules=['tribool'],
    package_data={'': ['LICENSE', 'README.rst']},
    install_requires=[],
    license=license,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
