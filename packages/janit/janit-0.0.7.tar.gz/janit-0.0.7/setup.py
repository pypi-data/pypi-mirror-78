import setuptools
import shutil
import os

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='janit',
    install_requires=['pyte'],
    version='0.0.7',
    author="David Hamner",
    author_email="ke7oxh@gmail.com",
    url="https://bitbucket.org/hackersgame/janit/src/master/",
    description='Terminal multiplexer/Menu',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #packages=setuptools.find_packages(),
    packages = ['.','Janit','Janit/core','Janit/cmd'],
    package_data={'Janit/core':['*.py'],'Janit/cmd':['*.py'],},
    entry_points={"console_scripts": ["janit=janit:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ]
)

