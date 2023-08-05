#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import setup


setup(
    name="crunchapilyb",
    version = "1.0.0",
    author="Yibang (Christopher) Liu",
    author_email="yibang.christopher.liu@gmail.com",
    description="A Crunch API by Christopher",
    license='Apache',
    url='https://github.com/ChristopherLiu618/CrunchAPI',
    packages=['crunchapilyb'],
    install_requires=['pandas', 'requests'],
    platforms=['any'],
    keywords='pandas, Crunch, API'
)