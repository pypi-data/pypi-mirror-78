#!/usr/bin/env python3

import os
import re

import setuptools


def get_version():
    root = os.path.dirname(os.path.abspath(__file__))
    init = open(os.path.join(root, "check_dep_updates", "__init__.py")).read()
    return re.compile(r"""__version__ = ['"]([0-9.]+.*)['"]""").search(init).group(1)


setuptools.setup(
    name="check_dep_updates",
    version=get_version(),
    python_requires=">=3.6",
    author="Adam Crowder",
    description="Dependency Update Checker for Pip",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cheeseandcereal/check-dep-updates",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={"check_dep_updates": ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=["pip"],
    entry_points={"console_scripts": ["cdu=check_dep_updates:main"]},
    license="Unlicense",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
    ],
    project_urls={
        "Source": "https://github.com/cheeseandcereal/check-dep-updates",
        "Bug Tracker": "https://github.com/cheeseandcereal/check-dep-updates/issues",
    },
)
