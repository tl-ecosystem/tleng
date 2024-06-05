from setuptools import setup, find_packages

setup(
    name='tleng',
    version='2.2.0.dev11',
    author='theolaos',
    description='TLeng is a python 2d game engine',
    packages=find_packages(),
    install_requires=[
        'pygame-ce',
        'numpy',
        'moderngl'
    ],
)