# -*- coding: utf-8 -*-
from distutils.core import setup

from setuptools import find_packages

setup(
    name='py-crypto-com-exchange-client',
    packages=find_packages(exclude=('tests',)),
    version='2020.09.05',
    description='Python client for Crypto.com exchange APIs',
    long_description='Python client for Crypto.com exchange APIs',
    long_description_content_type="text/markdown",
    author='Nikhil K Madhusudhan (nikhilkmdev)',
    author_email='nikhilkmdev@gmail.com',
    maintainer='Nikhil K Madhusudhan (nikhilkmdev)',
    maintainer_email='nikhilkmdev@gmail.com',
    install_requires=['py-simple-flow', 'requests==2.24.0', 'pandas', 'pyyaml'],
    keywords=['timeseries', 'history', 'python3'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
