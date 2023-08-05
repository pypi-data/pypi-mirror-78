#!/usr/bin/env python

# setuptools is required
from setuptools import setup

import subprocess

with open('README.md') as fp:
    description = fp.read()

# Versioning
try:
    DEVBUILD = subprocess.check_output(["git", "describe", "--tags"])
    with open('pandeia/engine/helpers/DEVBUILD', 'wb') as out:
        out.write(DEVBUILD)
except (subprocess.CalledProcessError) as err:
    print(err)

setup(
    # The package
    name="pandeia.engine",
    version="1.5.2",
    packages=["pandeia",
              "pandeia.engine",
              "pandeia.engine.defaults",
              "pandeia.engine.helpers",
              "pandeia.engine.helpers.schema"],
    # For PyPI
    description='Pandeia 3D Exposure Time Calculator compute engine',
    long_description=description,
    author='Adric Riedel, Klaus Pontoppidan, Craig Jones, Christopher Sontag, Oi In Tam Litten, Tim Pickering',
    #author_email='jwsthelp.stsci.edu',
    url='https://jwst.etc.stsci.edu',
    classifiers=["Intended Audience :: Science/Research",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Topic :: Scientific/Engineering :: Astronomy",
                 "Topic :: Software Development :: Libraries :: Python Modules"],
    # Other notes
    package_data={
        "pandeia.engine.defaults": ["*.json"],
        "pandeia.engine.helpers": ["DEVBUILD"]
        },
    include_package_data=True,
    install_requires=[
        "numpy>=1.17",
        "scipy",
        "astropy>=4",
        "photutils",
        "six",
        "synphot",
        "stsynphot",
        "setuptools"
    ],
    zip_safe=False
)
