import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="RsInstrument",
    version="1.4.0.29",
    description="VISA or Socket communication module for Rohde & Schwarz instruments",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Miloslav Macko",
    author_email="miloslav.macko@rohde-schwarz.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=(find_packages(include=['RsInstrument', 'RsInstrument.*'])),
    install_requires=["PyVisa"]
)