from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import os

AMPTOOLS_HOME = os.environ["AMPTOOLS_HOME"]
ROOT_HOME = os.environ["ROOTSYS"]
SRC = "/raid2/nhoffman/AmpToolsTools/src/ampwrapper"

amptools_extension = Extension(
        name="FitResults",
        sources=[SRC + "/fit/FitResults.pyx"],
        libraries=["AmpTools", "Physics", "MathCore", "Matrix"],
        library_dirs=[AMPTOOLS_HOME + "/AmpTools/lib", ROOT_HOME + "/lib"],
        include_dirs=[AMPTOOLS_HOME + "/AmpTools/IUAmpTools", ROOT_HOME + "/include"],
        language="c++")

setup(
    name="ampwrapper",
    version="0.0.1",
    author="Nathaniel Dene Hoffman",
    author_email="dene@cmu.edu",
    ext_modules=cythonize(amptools_extension),
    packages=find_packages('src'),
    package_dir={"": "src"},
    scripts=[SRC + "/amptools-activate",
             SRC + "/amptools-convert",
             SRC + "/amptools-fit",
             SRC + "/amptools-generate",
             SRC + "/amptools-link",
             SRC + "/amptools-study",
             SRC + "/amptools-plot",
             SRC + "/amptools-bootstrap",
             SRC + "/amptools-plot-bootstrap",
             SRC + "/amptools-search",
             SRC + "/amptools-select-thrown-topology",
             SRC + "/amptools-view-thrown-topologies",
             SRC + "/amptools-plot-angles"],
    install_requires=[
        'numpy',
        'cython',
        'enlighten',
        'simple_term_menu',
        'colorama',
        'pandas',
        'halo',
        'matplotlib',
        'particle',
        'tqdm',
        'uproot'
    ],
    zip_safe=False
)
