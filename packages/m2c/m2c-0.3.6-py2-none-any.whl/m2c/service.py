#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2018.11.28
from __future__ import print_function
import os

from .conf import *
from .helper import *
from .objtpl import *

SERVICE_TPL = '''
package {PKG_NAME}

import (
	"sync"
)

type {SRV_NAME}Service struct {{
}}

var (
	_{SRV_NAME_LOW}Service *{SRV_NAME}Service
	_once        sync.Once
)

func Init() {{
	_once.Do(func() {{
		_{SRV_NAME_LOW}Service = &{SRV_NAME}Service{{
		}}
	}})
}}

func GetInstance() *{SRV_NAME}Service {{
	if _{SRV_NAME_LOW}Service == nil {{
		panic("{SRV_NAME_LOW} service not init!!!")
	}}
	return _{SRV_NAME_LOW}Service
}}'''

SERVICE_EMPTY = '''
package {PKG_NAME}
'''

# srv 服务名, 小驼峰格式, 如user, eventSystem
def new_srv_code(srv):
    pkg = srv
    srv_name = upperFirst(srv)
    return SERVICE_TPL.format(PKG_NAME=pkg, SRV_NAME=srv_name, SRV_NAME_LOW=srv), SERVICE_EMPTY.format(PKG_NAME=pkg)
