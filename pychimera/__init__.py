#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pychimera import (main, patch_environ, enable_chimera, load_chimera,
                       enable_chimera_inline, chimera_view)

__author__ = "Jaime Rodríguez-Guerra"
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
