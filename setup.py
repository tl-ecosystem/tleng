from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

__name__ = "tleng"
__version__ = "2.2.0.dev12"
__author__ = "Theolaos"

# setup()
setup(
    name=__name__,
    version=__version__,
    author=__author__,
    description='TLeng is a python 2d game engine',
    packages=["tleng2"],
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        'pygame-ce',
        'numpy',
        'moderngl',
        'pymunk',
        'typing_extensions'
    ],
    entry_points={"console_scripts": ["tleng = tleng2.__main__:main"]},
)