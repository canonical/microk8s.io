"""
Several different loaders and dumpers for YAML under Python are implemented in the
respective submodules.


"""

from __future__ import print_function, division, absolute_import

import sys

from . import ordereddict

if sys.version_info[:2] < (2, 7):
    raise RuntimeError("You are using Python < 2.7. This is not supported. "
                       "Please upgrade your distribution and/or packages.")

__version__ = "0.5.5"
__author__ = 'Jonas Eschle "Mayou36", Johannes Lade "SebastianJL"'
__email__ = 'jonas.eschle@phynix.science, johannes.lade@phynix.science'

__all__ = ['ordereddict']
