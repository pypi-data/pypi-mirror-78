from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pt_lambdata", 
    version="0.0.2",
    author="Paul Teeter",
    author_email="paul-teeter@lambdastudents.com",
    description="A small collection of basic data utility functions.",
    long_description=long_description,
    long_description_content_type="text/markdown", # required if using a md file for long desc
    license="MIT",
    url="https://github.com/paulteeter/lambdata-paulteeter",
    packages=find_packages()
    )
    