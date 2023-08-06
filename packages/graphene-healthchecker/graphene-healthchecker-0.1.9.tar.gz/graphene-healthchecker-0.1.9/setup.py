#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = "0.1.9"
URL = "https://github.com/dactales/graphene-healthchecker"

setup(
    name="graphene-healthchecker",
    version=VERSION,
    description="Python library for RPC-healthchecking for graphene blockchains",
    download_url="{}/tarball/{}".format(URL, VERSION),
    author="ChainSquad GmbH",
    author_email="Fabian@dactales.com",
    maintainer="Fabian Schuh",
    maintainer_email="Fabian@dactales.com",
    url=URL,
    keywords=["graphene", "blockchain", "health", "api", "rpc"],
    packages=["graphene_health"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
    entry_points={"console_scripts": ["graphenehealth = graphene_health.cli:main"]},
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
