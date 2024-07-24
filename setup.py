from setuptools import setup, find_packages
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()


setup(
    name='sxtlac',
    version='0.0.2',
    author = 'Axel Ekman',  
    author_email = 'axel.ekman@iki.fi',
    url = '',
    description = 'A simple example python package.',
    long_description = long_description,
    license = "MIT license",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]   
)