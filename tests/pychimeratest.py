#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from glob import glob
import pytest
from pychimera import patch_environ, enable_chimera

if __name__ == '__main__':
    patch_environ()
    enable_chimera()
    pytest.main([a for arg in sys.argv[1:] for a in glob(arg)])
