#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from subprocess import check_output
from conftest import datapath
import sys

def test_script():
    out = check_output(['pychimera', datapath('helloworld.py')],
                       universal_newlines=True)
    assert out == 'Hello world! \n'


@pytest.mark.skipif(sys.platform == 'darwin', reason="Not supported on MacOS")
def test_script_args():
    out = check_output(['pychimera', datapath('helloworld.py'), '-h'],
                       universal_newlines=True)
    assert out == 'Hello world! -h\n'


def test_c_flag():
    out = check_output(["pychimera", "-c", "print('HelloWorld!')"],
                       universal_newlines=True)
    assert out == 'HelloWorld!\n'


@pytest.mark.skipif(sys.platform == 'darwin', reason="Not supported on MacOS")
def test_m_flag():
    out = check_output(['pychimera', '-m', 'helloworld'],
                       universal_newlines=True)
    assert out == 'Hello world! \n'
