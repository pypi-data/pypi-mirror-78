import setuptools

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AbstractModel",
    version="0.0.1",
    author="Guoyao Su",
    author_email="sgybupt@foxmail.com",
    description="An abstract model basic class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sgybupt/AbstractModel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
