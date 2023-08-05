from os import path
import sys
from setuptools import setup, find_packages
from setuptools.extension import Extension
import argparse

packages = [x for x in find_packages() if x != "test"]
setup(name='re3py',
      version='0.31',
      description="Relational ranking",
      url='https://github.com/petkomat/relational_ranking',
      python_requires='>3.6.0',
      author='Matej Petković, Blaž Škrlj',
      author_email='matej.petkovic@ijs.si',
      license='bsd-3-clause-clear',
      packages=packages,
      zip_safe=False,
      include_package_data=True,
      install_requires=['py4j', 'numpy'])
