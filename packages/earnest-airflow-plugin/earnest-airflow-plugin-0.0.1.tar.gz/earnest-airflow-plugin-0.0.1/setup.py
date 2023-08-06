#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import, print_function

import io
from os.path import dirname, join

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read a file and return the contents as a string."""
    return io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ).read()


setup(
    name="earnest-airflow-plugin",
    license="MIT License",
    description="Operators and Hooks for Airflow",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Earnest Research",
    author_email="python-package-index@earnestresearch.com ",
    url="https://github.com/EarnestResearch/airflow-plugin",
    python_requires=">=3.5",
    keywords=["airflow", "plugin"],
    project_urls={"Source": "https://github.com/EarnestResearch/airflow-plugin",},
    # Specify all the seperate packages, modules come automatically
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["apache-airflow[kubernetes]==1.10.10",],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={},
)
