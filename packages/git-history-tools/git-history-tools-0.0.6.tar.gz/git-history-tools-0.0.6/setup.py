#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from version import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()

setuptools.setup(
    name="git-history-tools",
    version=__version__,
    author='Orlando Tomás',
    author_email="orlando.tomas@hotmail.com",
    url="https://github.com/orltom/git-history-tools",
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    scripts=['githistory'],
    packages=['src'],
    python_requires='>=3.6',
)
