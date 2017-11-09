#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest

TESTPATH = os.path.dirname(os.path.abspath(__file__))


def datapath(path):
    return os.path.join(TESTPATH, path)