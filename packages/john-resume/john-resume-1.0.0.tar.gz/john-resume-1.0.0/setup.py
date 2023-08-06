import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="john-resume",
    version="1.0.0",
    author="John M. Gundersen",
    author_email="john@jmgundersen.com",
    scripts=['bin/john-resume'],
    description="A package for ease of access to the greatest resume available",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atomfinger/john_resume_pkg",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
        "Topic :: Other/Nonlisted Topic"
    ],
    python_requires='>=2.7',
)