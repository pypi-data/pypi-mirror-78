#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

# abandoned utility.path_type experiment
requirements = [
    # "python-magic==0.4.18"
]

setup_requirements = []

dev_requirements = {
    "dev": [
        "pip==20.2.2",
        "setuptools==49.2.0",
        "black==19.10b0",
        "bump2version",
        "docutils==0.16",
        "flake8==3.8.3",
        "nox==2020.5.24",
        "pytest==5.4.3",
        "Sphinx==3.1.2",
        "twine==3.2.0",
        "wheel==0.34.2",
        "check-manifest==0.42",
    ]
}

test_requirements = [
    "pytest>=3",
]

setup(
    author="Nate Marks",
    author_email="npmarks@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="libraries to make it easier to "
    "maniuplate files in a directory tree",
    install_requires=requirements,
    extras_require=dev_requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="treecrawl",
    name="treecrawl",
    packages=find_packages(include=["treecrawl", "treecrawl.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/natemarks/treecrawl",
    version="0.1.22",
    zip_safe=False,
)
