import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xkcd-comics",
    version="0.0.1",
    author="Brayo",
    author_email="vukubrian@gmail.com",
    description="A simple script for downloading all xkcd comics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brayo-pip/xkcd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)