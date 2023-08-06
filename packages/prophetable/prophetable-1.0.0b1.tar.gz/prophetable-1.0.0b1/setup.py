# -*- coding: utf-8 -*-
import io
import re

from collections import OrderedDict
from setuptools import setup, find_packages


with io.open("prophetable/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with open("README.md") as f:
    readme = f.read()

setup(
    name="prophetable",
    version=version,
    url="https://github.com/jucyai/prophetable",
    project_urls=OrderedDict(
        (
            ("Code", "https://github.com/jucyai/prophetable"),
            ("Issue tracker", "https://github.com/jucyai/prophetable/issues"),
        )
    ),
    license="MIT",
    author="Jiachen Yao",
    maintainer="Jiachen Yao",
    description="Define and run Prophet forecasting models using just a configuration file.",
    long_description_content_type="text/markdown",
    long_description=readme,
    packages=find_packages(include=["prophetable"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "cython",
        "pystan",
        "fbprophet",
        "red-panda>=1.0.0b1",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
