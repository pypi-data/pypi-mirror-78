# _*_ coding: utf-8 _*_
from setuptools import find_packages
from distutils.core import setup

setup(
    name='aptiviti-odbc',
    version='1.2.0',
    author='Daniel Fredriksen',
    author_email='df@etr.ai',
    packages=find_packages(),
    url='https://github.com/aptiviti/aptiviti-odbc',
    license='AGPLv3',
    description='Useful helper functions for constructing database queries'
)