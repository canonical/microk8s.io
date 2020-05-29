"""
Global settings for the behavior of the module.


"""

from __future__ import print_function, division, absolute_import

import sys

ALLOW_NON_C_FALLBACK = True

PY_LE_36 = sys.version_info[:2] <= (3, 6)
