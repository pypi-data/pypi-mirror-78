# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

REQUIREMENTS = [

]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = []

setup(
    name='ayewa',
    version=0.01,
    description='Core Module for Ayewa Application',
    author='siteshell.net',
    author_email='pdbethke@siteshell.net',
    url='https://github.com/pdbethke/erclient',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    # test_suite="test_settings.run",
)