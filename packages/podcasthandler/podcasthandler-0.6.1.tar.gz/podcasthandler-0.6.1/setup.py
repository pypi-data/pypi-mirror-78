#!/usr/bin/env python3

import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='podcasthandler',
    version='0.6.1',
    description='Easily play podcasts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fnt400/podcasthandler",
    author='Claudio Barca',
    author_email='claudio@barca.mi.it',
    scripts=['podcasthandler','podcasthandlerd'],
    packages=['podcasthnd'],
    classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
       "Operating System :: OS Independent",
    ],
    install_requires=["python-mpd2 ~= 1.0.0"],
    )
