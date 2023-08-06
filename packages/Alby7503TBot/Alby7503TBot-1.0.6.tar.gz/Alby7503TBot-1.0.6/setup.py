"""TBot setup.py"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Alby7503TBot",
    version="1.0.6",
    author="Alberto Vona",
    author_email="alberto.vona24@gmail.com",
    description="Lightweight telegram bot library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alby7503/TBot",
    license="GNU AGPLv3",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
