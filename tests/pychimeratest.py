#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytest
from pychimera import patch_environ, enable_chimera

if __name__ == '__main__':
    patch_environ()
    enable_chimera()
    pytest.main(sys.argv[1:])