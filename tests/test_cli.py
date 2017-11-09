#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from subprocess import check_output
from conftest import datapath

def test_script():
    out = check_output(['pychimera', datapath('helloworld.py')])
    assert out == 'Hello world!\n'

def test_c_flag():
    out = check_output(['pychimera', '-c', 'print("Hello world!")'])
    assert out == 'Hello world!\n'

def test_m_flag():
    out = check_output(['pychimera', '-m', 'helloworld'])
    assert out == 'Hello world!\n'
