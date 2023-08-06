from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="simpycard",
    version="0.0.2",
    author="crazy6973",
    description="Package for simple playing-cards",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/crazy6973/simpycard/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
