import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bible_reference", # Replace with your own username
    version="1.1",
    author="Diedrich Vorberg",
    author_email="diedrich@tux4web.de",
    description="This module implements classes that I have developed to parse and output Bible references.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dvorberg/bible_reference",
    
    packages=setuptools.find_packages(),
    
    package_data={"": ["*.names", "*.canon", "*.info"]},
    include_package_data=True,
    
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)

