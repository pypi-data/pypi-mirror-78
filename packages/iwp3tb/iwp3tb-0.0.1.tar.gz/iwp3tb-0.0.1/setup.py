#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iwp3tb",
    version="0.0.1",
    author="Ish West",
    author_email="optimistcli@yandex.kz",
    description="Ish West Python 3 Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/optimistiCli/ishwest_py3_toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)