"""
Extends `openpyxl` classes for easier operation on Excel tables.
"""

from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyxltab",
    version="0.1.0",
    description=("Extends openpyxl for easier operation on Excel tables."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blakeNaccarato/pyxltab",
    author="Blake Naccarato",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=["openpyxl>=3.0.5"],
)
