from __future__ import print_function
import os
import sys
from .conf import *
from .helper import *

if sys.argv[-1] == '-v3' or sys.argv[-1] == '-v4':
    set_version(sys.argv[-1].strip('-'))
    sys.argv = sys.argv[:-1]
else:
    set_version(m2c_cliversion())

print('m2c_version:', m2c_version())
print('m2c_cliversion:', M2C_VERSION)
print('py3_version:', IS_PY3())

if os.path.exists('.env'):
    for line in open('.env'):
        items = line.split('=')
        if len(items) < 2:  # hander '=' in value(query string)
            continue
        print('load env:', items[0], '='.join(items[1:]))
        os.environ[items[0].strip()] = '='.join(items[1:]).strip()
