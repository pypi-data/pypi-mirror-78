#!/usr/local/env python3
import setuptools
##############################################

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read()

setuptools.setup(
     name='bio_pyminer_norm',  
     version='0.2',
     author="Scott Tyler",
     author_email="scottyler89@gmail.com",
     description="PyMINEr Norm: A normalization package for scRNAseq",
     long_description=long_description,
     long_description_content_type="text/markdown",
     install_requires = install_requires,
     url="https://scottyler892@bitbucket.org/scottyler892/pyminer_norm",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Affero General Public License v3",
         "Operating System :: OS Independent",
     ],
 )
