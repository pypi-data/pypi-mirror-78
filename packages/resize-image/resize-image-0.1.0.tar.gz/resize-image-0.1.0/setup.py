# -*- coding: utf-8 -*-
 
 
"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('resize/resize.py').read(),
    re.M
    ).group(1)
 
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "resize-image",
    packages = ["resize"],
    entry_points = {
        "console_scripts": ['resize-image = resize.resize:main']
        },
    version = version,
    description = "Commandline utility to resize an image.",
    long_description = long_descr,
    author = "Jay Mu",
    author_email = "me@jaymu.com",
    url = "https://github.com/jaymu53/resize-image",
     install_requires=[           
          'PIL',
          'resizeimage',
      ],    
)

