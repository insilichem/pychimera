#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import platform as PLATFORM, exit

_INSTRUCTIONS = ('Please, create an environment variable CHIMERADIR set '
                 'to your Chimera installation path, or softlink the '
                 'Chimera binary to somewhere in your $PATH.')

if PLATFORM.startswith('win') or PLATFORM == 'cygwin':
    from .win import *
elif PLATFORM.startswith('linux'):
    from .linux import *
elif PLATFORM.startswith('darwin'):
    from .osx import *
else:
    exit('ERROR: Platform `{}` not supported.\n{}'.format(PLATFORM, _INSTRUCTIONS))


def patch_environ_for_platform(*args, **kwargs):
    _patch_envvars(*args, **kwargs)
    _patch_paths(*args, **kwargs)
    _patch_libraries(*args, **kwargs)


__all__ = ('_INSTRUCTIONS',
           'CHIMERA_BINARY',
           'CHIMERA_PREFIX',
           'CHIMERA_LOCATIONS',
           'NULL',
           'patch_environ_for_platform',
           'launch_ipython')
