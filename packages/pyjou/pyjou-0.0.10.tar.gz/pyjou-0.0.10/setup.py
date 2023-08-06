from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name="pyjou",
    version="v0.0.10",
    author="Nick Kuzmenkov",
    author_email="nickuzmenkov@yahoo.com",
    description="Fluent Journal API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/nickuzmenkovorg/pyjou",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)