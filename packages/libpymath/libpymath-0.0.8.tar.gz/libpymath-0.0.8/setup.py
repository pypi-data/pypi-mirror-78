# -*- coding: utf-8 -*-
from pathlib import Path

try:
    from setuptools import setup, Extension, find_packages
except ImportError:
    from distutils.core import setup, Extension

    def find_packages(where='.'):
        return [folder.replace("/", ".").lstrip(".")
                for (folder, _, fils) in os.walk(where)
                if "__init__.py" in fils]

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')

ext_modules = [
    Extension(
        "libpymath.core.testModule",
        ["LibPyMath/LibPyMathModules/testModule.c"],
    ),
    Extension(
        "libpymath.core.matrix",
        ["LibPyMath/LibPyMathModules/matrixModule.c"],
    )
]

setup(
    name="libpymath",
    version="0.0.8",
    description="A general purpose Python math module",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Toby Davis",
    author_email="pencilcaseman@gmail.com",
    url="https://www.github.com/pencilcaseman/gpc",
    ext_modules=ext_modules,
    packages=["libpymath"] + ["libpymath." + mod for mod in find_packages("libpymath")],
    keywords=["math", "matrix", "network", "neural network",
    		  "libpymath", "pymath", "libmath"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
