from setuptools import setup
from Cython.Build import cythonize

# Build using: python cython_helpers/setup.py build_ext --inplace

setup(
    name='Intersection helper',
    ext_modules=cythonize("intersection.pyx", language_level="3"),
    zip_safe=False,
)