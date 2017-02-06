# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='FuelManagement',
    version='16.4.29',
    description='FuelManagement Software. Final OOP Project.',
    long_description=readme,
    author='Tirdad Kiafar',
    author_email='kiafr@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

