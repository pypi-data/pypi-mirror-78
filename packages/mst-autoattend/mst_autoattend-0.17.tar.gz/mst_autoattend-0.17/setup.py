import os
import sys
from distutils.core import setup

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

def read(file_name):
    """
    Reads data from file for the description parameter of `setup()`.
    Parameters
    ----------
    file_name: str
        path to the README.md file.
    Returns
    -------
    str
        the text contained in the given file.
    """
    with open(file_name, mode='r') as readme:
        return readme.read()


# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

setup(name='mst_autoattend',
    version='0.17',
    packages=find_packages(),
    description='A tool to attend the MS Team meetings for you!',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Shivam Kumar Jha',
    author_email='coffee@thealphadollar.me',
    url='https://github.com/thealphadollar/MS-Teams-Class-Attender',
    install_requires=[
    'webdriver_manager==3.2.1',
    'selenium==3.141.0',
    ],
    entry_points={
        'console_scripts': [
            'mst_autoattend=mst_autoattend:main',
        ],
    },
    include_package_data=True
)
