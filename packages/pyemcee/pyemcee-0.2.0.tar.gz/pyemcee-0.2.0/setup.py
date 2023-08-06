#!/usr/bin/env python

#
# Setup script for pyemcee
#

import os
import codecs
try:
      from setuptools import setup
except ImportError:
      from distutils.core import setup

import pyemcee

with codecs.open('README.rst', 'r', 'utf-8') as fd:
    setup(name='pyemcee',
          version=pyemcee.__version__,
          description = 'pyemcee: Python implementation of the affine-invariant MCMC Hammer',
          long_description=fd.read(),
          author='Ashkbiz Danehkar',
          author_email='ashkbiz.danehkar@students.mq.edu.au',
          url='https://mcfit.github.io/pyemcee/',
          download_url = 'https://github.com/mcfit/pyemcee',
          keywords = ['pyemcee', 'MCMC', 'emcee', 'Python', 'ensemble sampler', 'hammer'],
          license='http://www.gnu.org/licenses/gpl.html',
          platforms=['any'],
          packages=['pyemcee'],
          package_data={'pyemcee': ['*.txt', 'text/*.readme']},
          install_requires=['numpy','scipy','matplotlib'],
         )

