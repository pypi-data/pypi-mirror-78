# -*- coding: utf-8 -*-
from distutils.core import setup

from setuptools import find_packages

setup(
    name='py-influxdb',
    packages=find_packages(exclude=('tests',)),
    version='2020.09.04',
    description='Python Client for Influx DB',
    long_description='Leverages the REST APIs exposed by Influx DB Server to write/query data',
    long_description_content_type="text/markdown",
    author='Nikhil K Madhusudhan (nikhilkmdev)',
    author_email='nikhilkmdev@gmail.com',
    maintainer='Nikhil K Madhusudhan (nikhilkmdev)',
    maintainer_email='nikhilkmdev@gmail.com',
    install_requires=['requests==2.24.0'],
    keywords=['influxdb', 'influx-db', 'influx', 'timeseries', 'python3'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
