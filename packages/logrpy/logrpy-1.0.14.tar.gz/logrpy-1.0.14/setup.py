from setuptools import setup, find_packages
from m2r import convert


with open("README.md", "r") as fh:
    long_description = fh.read()

long_description = convert(long_description)


setup(
    name='logrpy',
    version='1.0.14',
    author='Kozhurkin Dima',
    author_email='kozhurkin.dima@gmail.com',
    description='Logr client library for Python.',
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'pycryptodome',
        'colorama',
        'psutil',
    ],
    url='https://github.com/504dev/logr-python-client',
    include_package_data=True
)
