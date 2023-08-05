#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Trailblazer is a tool to manage and track state of analyses.

You can install it from PyPI as follows::
    pip install trailblazer

For more detailed instructions, run :code:`trailblazer --help`

See the GitHub repo for documentation:
`Clinical-Genomics/analysis <https://github.com/Clinical-Genomics/analysis>`_
"""
# To use a consistent encoding
import codecs
import os

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

# Shortcut for building/publishing to Pypi
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


def parse_reqs(req_path="./requirements.txt"):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with codecs.open(req_path, "r") as handle:
        # remove comments and empty lines
        lines = (
            line.strip() for line in handle if line.strip() and not line.startswith("#")
        )
        for line in lines:
            # check for nested requirements files
            if line.startswith("-r"):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])
            else:
                # add the line as a new requirement
                install_requires.append(line)
    return install_requires


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):

    """Set up the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest

        sys.exit(pytest.main(self.test_args))


setup(
    name="trailblazer",
    # Versions should comply with PEP440. For a discussion on
    # single-sourcing the version across setup.py and the project code,
    # see http://packaging.python.org/en/latest/tutorial.html#version
    version="6.8.4",
    description=("Track MIP analyses."),
    long_description=__doc__,
    # What does your project relate to? Separate with spaces.
    keywords="analysis development",
    author="Robin Andeer",
    author_email="robin.andeer@scilifelab.se",
    license="MIT",
    # The project's main homepage
    url="https://github.com/Clinical-Genomics/analysis",
    packages=find_packages(exclude=("tests*", "docs", "examples")),
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    include_package_data=True,
    # package_data={
    #     'taboo': [
    #         'server/genotype/templates/genotype/*.html',
    #     ]
    # },
    zip_safe=False,
    # Although 'package_data' is the preferred approach, in some case you
    # may need to place data files outside of your packages.
    # In this case, 'data_file' will be installed into:
    # '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    # Install requirements loaded from ``requirements.txt``
    install_requires=parse_reqs(),
    tests_require=[
        "pytest",
    ],
    cmdclass=dict(
        test=PyTest,
    ),
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and
    # allow pip to create the appropriate form of executable for the
    # target platform.
    entry_points={
        "console_scripts": [
            "trailblazer = trailblazer.cli:base",
        ]
    },
    # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
    ],
)
