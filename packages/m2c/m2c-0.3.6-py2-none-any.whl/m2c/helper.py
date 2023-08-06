#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2018.11.28
from __future__ import print_function
import os
import sys
import json

def IS_PY3():
    return sys.version_info >= (3, 0)

def assert_error(exp, msg, lineno, line):
    if exp:
        return
    err = 'line(%s): %s, error: %s' % (lineno, line, msg)
    raise Exception(err)

def writeCode(path, code):
    os.system('mkdir -p %s' % os.path.dirname(path))
    if IS_PY3():
        code = code.encode('utf-8')
    with open(path, 'wb') as f:
        f.write(code)

def appendCode(path, code):
    os.system('mkdir -p %s' % os.path.dirname(path))
    if IS_PY3():
        code = code.encode('utf-8')
    with open(path, 'ab') as f:
        f.write(code)

def getCodeFuncs(path):
    funcs = []
    for line in open(path, 'rb'):
        if IS_PY3():
            line = line.decode('utf-8')
        line = line.strip()
        if not line.startswith('func '):
            continue
        
        item, _ = line.split('(', 1)
        items = item.split()
        if len(items) != 2:
            print('无效的函数定义:%s' % line)
            continue
        funcs.append(items[1])
    return funcs

def upperFirst(s):
    if len(s) in (0, 1):
        return s.upper()
    if '_' in s:
        items = s.split('_')
        name = ''
        for item in items:
            name += upperFirst(item)
        return name
    return s[0].upper() + s[1:]

def is_valid_var(s):
    if len(s) == 0:
        return False
    if s[0].isdigit():
        return False
    s = s.replace('_', '')
    return s.isalnum()

def is_m2c():
    return os.path.exists('.m2c')

def m2c_version():
    if not is_m2c():
        return None
    
    d = json.loads(open('.m2c', 'rb').read())
    return d['__version__']

def m2c_cliversion():
    if not is_m2c():
        return None
    
    d = json.loads(open('.m2c', 'rb').read())
    return d.get('__cliversion__', 'v2')

def update_m2c(new_version, cli_version='v2'):
    d = json.loads(open('.m2c', 'rb').read())
    d['__version__'] = new_version
    d['__cliversion__'] = cli_version
    if IS_PY3():
        open('.m2c', 'wb').write(json.dumps(d, indent=2).encode('utf-8'))
    else:
        open('.m2c', 'wb').write(json.dumps(d, indent=2))
