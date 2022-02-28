from setuptools import setup
from Cython.Build import cythonize
import numpy

# Build using: python c_setup.py build_ext --inplace

setup(
    name='Top result helper',
    ext_modules=cythonize("top_results_helper.pyx", language_level="3"),
    zip_safe=False,
    include_dirs=[numpy.get_include()]
)