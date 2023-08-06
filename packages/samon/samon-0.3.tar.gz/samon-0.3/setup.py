#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name='samon',
    version='0.3',
    description='Samon (salmon) XML based templating engine',
    license='BSD',
    author='Bence Lovas',
    author_email='lovas.bence@doculabs.io',
    url='https://github.com/doculabs/samon',
    download_url='https://github.com/doculabs/samon',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['simpleeval==0.9.10'],
)
