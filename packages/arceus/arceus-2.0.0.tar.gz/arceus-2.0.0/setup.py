# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="arceus",
    version="2.0.0",
    description="Minecraft name sniper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL-3.0-or-later",
    author="Aquild",
    packages=find_packages(),
    install_requires=[
        "requests",
        "requests-random-user-agent",
        "tcp-latency",
        "bs4",
        "pause",
        "click",
        "PyInquirer",
        "colorama",
        "termcolor",
        "pyfiglet",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    entry_points={"console_scripts": ["arceus=arceus.cli:cli"]},
)
