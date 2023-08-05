#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: mar. juin 16 08:14:40 CEST 2020 -*-
# -*- copyright: GH/IPHC 2020 -*-
# -*- file: __init__.py -*-
# -*- purpose: -*-

'''
Importing the wrapping functions
'''

import warnings
import sys


if sys.version_info >= (3, 6):
    # good boy
    pass
elif sys.version_info < (3, 6):
    warnings.warn("# WARNING: faster module has been designed for python 3.6 and higher")
elif not sys.version_info <= (3, 5):
    raise RuntimeError("Module should be used with python 3.6 or higher")

from .ascii_data_file import data_file

# EOF
