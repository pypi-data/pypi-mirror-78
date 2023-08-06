# Check Dependency Updates

[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License](https://img.shields.io/badge/license-Unlicense-informational.svg)](https://github.com/cheeseandcereal/check-dep-updates/blob/master/UNLICENSE)
[![pypi Version](https://img.shields.io/pypi/v/check-dep-updates)](https://pypi.org/project/check-dep-updates/)

This is a tool used for checking dependency versions in [requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files) style files.
Inspired by tools such as [npm-check-updates](https://www.npmjs.com/package/npm-check-updates).

Note this is a very simple and targeted tool. It will look at a requirements.txt file, and print which dependencies with a version are out of date, with the current latest version. This is in contrast to tools like [pur](https://github.com/alanhamlett/pip-update-requirements) or [pip-upgrader](https://github.com/simion/pip-upgrader) etc, as this is trying to only do a single thing.

If you have pip and installed, this does not require any other dependencies, as it uses pip's native vendored dependencies in order to keep footprint down.
This also allows this tool to be 'portable' in the sense where you can just take the [single python file](check_dep_updates/__init__.py) and use it on any machine with pip installed.

## Install

You can install this with pip:

```sh
pip install check-dep-updates
```

If you do this, it should automatically get installed and be available with the `cdu` command

Alternatively, you can copy and use the single python file \_\_init\_\_.py directly on any system with pip installed.

## Usage

Once installed, the `cdu` command should be the aliased commmand.

### Within A Project Directory

```sh
$ ls
my_app/
requirements.txt
$ cdu
Newer version of requests: 2.24.0
Done
```

### With a Specific requirements File

```sh
$ cdu -f dev_requirements.txt
Newer version of black: 19.10b0
Done
```
