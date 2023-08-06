"""
pyemcee - Python implementation of the affine-invariant MCMC Hammer
"""

__all__ = ["hammer","find_errors"]

from .pyemcee import hammer, find_errors
from .version import __version__

import sys
from numpy.version import version as numpy_version

if sys.version_info[0:2] < (2, 6):
    log_.warn('pyemcee requires Python version >= 2.6, but it is version {0}'.format(sys.version_info), calling='pyemcee')
try:
    if [int(n) for n in (numpy_version.split('.')[:3])] < [1, 5, 1] :
        log_.warn('pyemcee Numpy version >= 1.5.1, but it is version {0}'.format(numpy_version), calling='pyemcee')
except:
    log_.warn('Cannot find Numpy version {0}, report the bug'.format(numpy_version), calling='pyemcee')
    


