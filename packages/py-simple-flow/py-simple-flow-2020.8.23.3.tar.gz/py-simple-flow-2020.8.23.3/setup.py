# -*- coding: utf-8 -*-
from distutils.core import setup

from setuptools import find_packages

setup(
    name='py-simple-flow',
    packages=find_packages(exclude=('tests',)),
    version='2020.08.23.3',
    description='Simple data processing (ETL) library with support for multi-processing',
    long_description='''### Python Simple Flow 
    - Simple framework with a defined structure for data processing with support for multi-process
    - Data processing flow is split into four phases:
        - Source: Fetch the data from a source 
        - Ingress: Register the data received, log or in DB for trace-ability
        - Transform: Business logic of transforming the data to your business needs
        - Egress: Push the data to downstream or your storage
    - Processing can be done in one process, like running it in-process or in multi processing mode
    - Mode to be chosen depends on the task you are doing
    - Easy setting up logger even in multi processing mode
    ''',
    long_description_content_type="text/markdown",
    author='Nikhil K Madhusudhan (nikhilkmdev)',
    author_email='nikhilkmdev@gmail.com',
    maintainer='Nikhil K Madhusudhan (nikhilkmdev)',
    maintainer_email='nikhilkmdev@gmail.com',
    install_requires=['pandas'],
    keywords=[
        'etl',
        'multi processing',
        'data',
        'processing',
        'data processing',
        'data flow',
        'python3',
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
