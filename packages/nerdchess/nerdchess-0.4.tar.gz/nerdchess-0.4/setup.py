"""Info for setup tools."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nerdchess",
    version="0.4",
    author="j wizzle",
    author_email="info@hossel.net",
    description="A Python chess engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwizzle/NerdChess",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
