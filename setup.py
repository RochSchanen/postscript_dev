# file: setup.py
# content: setup file for package 'm'
# created: 2024 April 11
# modified:
# modification:
# author: Roch Schanen
# comment:

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pslib",
    version="0.0.0",
    author="Roch Schanen",
    author_email="r.schanen@lancaster.ac.uk",
    description="postscript code generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RochSchanen/pslib",
    packages = ['pslib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        # "License :: OSI Approved :: MIT License",
    ],
    install_requires=[],
    python_requires='>=3.0'
)
