import os
import sys

from setuptools import setup, find_packages


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()

print("setup.py prefix:", sys.prefix)

setup(
    name="hmd",
    version="0.7",

    # Requires python3.5
    python_requires=">=3.5",

    # Automatically import packages
    packages=find_packages(),

    # Include the files specified in MANIFEST.in in the release archive
    include_package_data=True,

    # Scripts to install to the user executable path.
    entry_points={
        "console_scripts": [
            "hmd = hmd.__main__:main",
        ]
    },


    # Metadata
    author="Stefano Dottore",
    author_email="docheinstein@gmail.com",
    description="Simple markdown language and processor for write and render document similar to man pages, from command line or from Python",
    long_description=read('README.MD'),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="hmd",
    url="https://github.com/Docheinstein/hmd",
    install_requires=[]
)