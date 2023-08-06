#!/usr/bin/env python

import setuptools


setuptools.setup(
    name="ochs",
    packages=["ochs"],
    version="0.2-alpha",
    license="MIT",
    description="Tool for building static blogs based on Markdown posts, YAML files and handwritten HTML templates.",
    author="Victhor Sartório",
    author_email="victhor@vsartor.com",
    url="https://github.com/vsartor/ochs",
    keywords=["blog", "website", "generator", "cli"],
    install_requires=[
        "click",
        "pyyaml",
        "markdown",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Typing :: Typed",
    ],
    entry_points="""
        [console_scripts]
        ochs=ochs.cli:blog
    """,
)
