from setuptools import setup
from rawprasslib import __version__

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name="rawprasslib",
    version=__version__,
    author="Erik Andris, Jan Zelenka",
    author_email="3yanyanyan@gmail.com",
    description="Thermo/Finnigan .raw file format reader",
    long_description=long_description,
    url="https://gitlab.science.ru.nl/jzelenka/rawprasslib",
    packages=['rawprasslib'],
    license="MIT",
    platforms=["OS Independent"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        ],
    install_requires=['numpy']
    )
