## EXAMPLE SETUP

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enginEcon",
    version="0.0.1",
    author="Daniel Tan",
    author_email="cookiedan42@gmail.com",
    description="helper functions for Engineering Economy problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cookiedan42/EnginEcon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
