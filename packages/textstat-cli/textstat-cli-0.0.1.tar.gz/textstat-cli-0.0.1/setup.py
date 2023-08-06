#!/usr/bin/env python

from distutils.core import setup

setup(
    name="textstat-cli",
    version="0.0.1",
    description="A CLI wrapper for the textstat library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Matt Copperwaite",
    author_email="matt@copperwaite.net",
    url="https://github.com/yamatt/python3-textstat-cli",
    packages=["textstat_cli"],
    scripts=["scripts/textstat"],
)
