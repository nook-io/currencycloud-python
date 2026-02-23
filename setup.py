#!/usr/bin/env python

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="currency_cloud",
    version="5.7.1",
    license="MIT",
    description="Async Python SDK for the Currencycloud API.",
    long_description="",
    author="Johnny Deuss",
    author_email="johnny@nook.io",
    url="https://github.com/nook-io/currencycloud-python",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[],
    install_requires=["httpx", "PyYAML", "deprecation"],
    tests_require=["pytest", "mock", "pytest-httpx", "vrc"],
    test_suite="tests",
)
