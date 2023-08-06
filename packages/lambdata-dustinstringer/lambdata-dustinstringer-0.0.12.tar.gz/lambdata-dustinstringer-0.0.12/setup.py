"""This module is for setting up the package for pypi."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambdata-dustinstringer",  # Replace with your own username
    version="0.0.12",
    author="Dustin Stringer",
    author_email="dustinstringer92@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dustin-py/lambdata-dustinstringer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

#  python3 setup.py sdist bdist_wheel
#  twine upload --skip-existing  dist/*
