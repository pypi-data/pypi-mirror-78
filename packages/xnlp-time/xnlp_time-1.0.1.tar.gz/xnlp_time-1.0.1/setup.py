#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time  : 2020/5/29 11:50
# @Author: xnlp
from setuptools import setup, find_packages
from xnlp_time import __version__, __author__, __description__, __email__, __names__, __url__

with open('README.md', encoding='utf-8') as f:
    long_text = f.read()

# with open('requirements.txt', encoding='utf-8') as f:
#     install_requires = f.read().strip().splitlines()

setup(
    name=__names__.lower(),
    version=__version__,
    description=__description__,
    long_description=long_text,
    long_description_content_type="text/markdown",
    url=__url__,
    author=__author__,
    author_email=__email__,
    license='MIT Licence',
    packages=find_packages(),
    platforms='any',
    package_data={'': ['*']},
    install_requires=['arrow==0.15.5', 'pyunit-calendar==2019.5.9', 'pyunit-gof==2020.3.11', 'matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
)
