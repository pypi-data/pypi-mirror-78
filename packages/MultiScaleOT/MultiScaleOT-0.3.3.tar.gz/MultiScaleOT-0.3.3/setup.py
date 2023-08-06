import setuptools
#from cmake_setuptools import *

import os
import re
import sys
import sysconfig
import platform
import subprocess

#from distutils.version import LooseVersion
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [\
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,\
                '-DPYTHON_EXECUTABLE=' + sys.executable]
        build_args=[]


        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args,
                              cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)
        print()  # Add an empty line for cleaner output


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="MultiScaleOT", # Replace with your own username
    version="0.3.3",
    author="Bernhard Schmitzer",
    author_email="bernhard.schmitzer@tum.de",
    description="A package with coarse-to-fine solvers for optimal transport problems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bernhard-schmitzer/MultiScaleOT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X"
    ],
    python_requires='>=3.4',
    zip_safe=False,
    #packages=["MultiScaleOT"],
    #package_dir={'MultiScaleOT': '.'},
    #package_data={'MultiScaleOT': ['example-data/*']},
    #include_package_data=True,
    ext_modules=[CMakeExtension('MultiScaleOT',\
            sourcedir="./src")],
    cmdclass={'build_ext': CMakeBuild}
    )



