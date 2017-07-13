import sys
import os
from setuptools import setup, find_packages


version = '0.0.13'

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as file:
    long_description = file.read()

required_modules = ['requests', 'python-dateutil', 'six', 'cached-property']

if sys.version_info < (3, 4):
    required_modules.append('enum34')

setup(
    name="pynder",
    version=version,
    packages=find_packages(exclude=('examples')),
    install_requires=required_modules,
    package_data={'': ['*.rst']},
    author="Charlie Wolf",
    author_email="charlie@wolf.is",
    description="A client for the tinder api",
    license="Tequila-ware Rev.44",
    keywords=["tinder", "online dating"],
    url="https://github.com/charliewolf/pynder",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
