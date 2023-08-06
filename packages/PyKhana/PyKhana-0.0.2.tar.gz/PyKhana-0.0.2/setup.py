import setuptools

with open("README.md", "r", encoding="utf-8",errors='ignore') as fh:
    long_description = fh.read()
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

setuptools.setup(
    name = "PyKhana",
    version = "0.0.2",
    author = "Dipam Paul",
    author_email = "dipampaul17@gmail.com",
    description = ("An demonstration of how to implement Gaussian Integer operations in Python."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    keywords = "PyKhana, GaussianInt",
    url = "https://github.com/dipampaul17/PyKhana",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
   
)