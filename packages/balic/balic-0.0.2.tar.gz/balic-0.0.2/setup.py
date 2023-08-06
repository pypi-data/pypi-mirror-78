#!/usr/bin/env python
from os.path import join

PROJECT = "balic"

from balic import Balic

VERSION = Balic.__version__


from setuptools import setup, find_packages

try:
    long_description = open("README.rst", "rt").read()
except IOError:
    long_description = ""


def load_requirements(requirements_file):
    reqs = []
    with open(join("requirements", requirements_file)) as requirements:
        for requirement in requirements.readlines():
            if requirement.strip() and not requirement.strip().startswith("#"):
                reqs.append(requirement)
    return reqs

requirements_base = load_requirements("base.txt")

setup(
    name=PROJECT,
    version=VERSION,
    description="Balic - Command-line Linux Containers Toolset",
    long_description=long_description,
    author="Marek Kuziel",
    author_email="marek@kuziel.info",
    url="https://gitlab.com/markuz/balic",
    download_url="https://gitlab.com/markuz/balic/-/archive/master/balic-master.tar.bz2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Other Audience",
        "Environment :: Console",
    ],
    platforms=["Any"],
    scripts=[],
    provides=[],
    install_requires=requirements_base,
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["balic = balic.main:main"],
        "balic": [
            "build = balic.build:Build",
            "create = balic.create:Create",
            "destroy = balic.destroy:Destroy",
            "ls = balic.ls:Ls",
            "pack = balic.pack:Pack",
        ],
    },
    zip_safe=False,
)
