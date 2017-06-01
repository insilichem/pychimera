#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pychimera


def run():
    pychimera.main()
    update_dict = {k: v for (k, v) in pychimera.__dict__.iteritems()
                   if k not in globals()}
    globals().update(update_dict)


if "__main__" == __name__:
	run()