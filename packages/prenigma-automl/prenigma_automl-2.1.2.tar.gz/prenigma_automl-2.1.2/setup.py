# Copyright (C) 2019-2020 Prenigma <hello@predapp.com>
# License: MIT, hello@predapp.com

from prenigma_automl.utils import version
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="prenigma_automl",
    version=f"{version()}",
    description="prenigma_automl - An open source, low-code machine learning library.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/prenigma-auto-ml/prenigma_automl",
    author="Prenigma",
    author_email="hello@predapp.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["prenigma_automl"],
    include_package_data=True,
    install_requires=required
)