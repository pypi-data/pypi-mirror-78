#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2018.11.28
 
import os


M2C_VERSION = 'v2'
MOD = 'gopher'
PROJECT_DIR = os.getcwd()
GOPHER_DIR = os.path.join(PROJECT_DIR, MOD)
APP_DIR = os.path.join(GOPHER_DIR, 'app')
SERVICE_DIR = os.path.join(GOPHER_DIR, 'service')
APIDOC_DIR = os.path.join(PROJECT_DIR, 'doc/api')
M2C_PATH = os.path.join(PROJECT_DIR, '.m2c')
BUILD_DIST = os.path.join(PROJECT_DIR, 'dist')
SWAGGER_PATH = os.path.join(GOPHER_DIR, "app/router/swagger.go")
SWAGGER_YAML_PATH = os.path.join(GOPHER_DIR, "app/router/swagger.yaml")
GOMOD_PATH = os.path.join(GOPHER_DIR, 'go.mod')
APIMODEL_PATH = os.path.join(PROJECT_DIR, 'apimodel.txt')
OBJMODEL_PATH = os.path.join(PROJECT_DIR, 'objmodel.txt')
M2C_PROJECT_INIT_URL = 'https://dat-pub.oss-cn-hangzhou.aliyuncs.com/m2c/m2c-0.0.3.zip'
M2C_PROJECT_INIT_URL_V4 = 'https://dat-pub.oss-cn-hangzhou.aliyuncs.com/m2c/m2c-0.1.3.zip'
M2C_PROJECT_INIT_NAME = os.path.basename(M2C_PROJECT_INIT_URL)
LOG_HOME = '/data/log'

TYPEMAPPING = {
    'str': 'string',
    '[]str': '[]string',
    'string': 'string',
    '[]string': '[]string',
    'int': 'int64',
    'int32': 'int32',
    'int64': 'int64',
    'long': 'int64',
    'float': 'float64',
    'float64': 'float64',
    'float32': 'float32',
    'double': 'float64',
    '[]int': '[]int64',
    'int32': 'int32',
    '[]int32': '[]int32',
    'int64': 'int64',
    '[]int64': '[]int64',
    'long': 'int64',
    '[]long': '[]int64',
    'float': 'float64',
    '[]float': '[]float64',
    'float64': 'float64',
    '[]float64': '[]float64',
    'float32': 'float32',
    '[]float32': '[]float32',
    'double': 'float64',
    '[]double': '[]float64',
    'time': 'time.Time',
    'bool': 'bool',
    '[]bool': '[]bool',
    'any': 'interface{}',
    'dict': 'map[string]interface{}',
    'json': 'map[string]interface{}',
    'JsonNode': 'map[string]interface{}',
}

APIDOC_TYPE = {
    'int64': 'Number',
    'int32': 'Number',
    'int': 'Number',
    'float': 'Number',
    'float32': 'Number',
    'float64': 'Number',
    '[]float': 'Number[]',
    '[]float32': 'Number[]',
    '[]float64': 'Number[]',
    '[]int64': 'Number[]',
    '[]int32': 'Number[]',
    '[]int': 'Number[]',
    'str': 'String',
    '[]str': 'String[]',
    'string': 'String',
    '[]string': 'String[]',
    'interface{}': 'Object',
    '[]interface{}': 'Object[]',
    'bool': 'Boolean',
    '[]bool': 'Boolean[]',
    'object': 'Object',
    '[]object': 'Object[]',
    'number': 'Number',
    '[]number': '[]Number',
    'number[]': 'Number[]', # old
    'object[]': 'Object[]', # old
}

OPENAPIDOC_TYPE = {
    'int64': 'number',
    'int32': 'number',
    'int': 'number',
    'float': 'number',
    'float32': 'number',
    'float64': 'number',
    'str': 'string',
    'string': 'string',
    'interface{}': 'object',
    'bool': 'boolean',
    'object': 'object',
    'number': 'number',
}

AUTH_TYPE = ['userAuth', 'adminAuth', None]
PROTO_TYPE = ['json', 'raw', 'reqRaw', 'respRaw', None]

TAB_WIDTH = 4
API_MAX_DEEP_NUM = 2


OBJ_ALLOWED_PREFIX = ["&", "@", "^"]
OBJ_REF_TYPE_MANAGE = "manage"
OBJ_REF_TYPE_REF = "refer"
OBJ_CONTAINER_TYPE_BASIC = "basic"
OBJ_CONTAINER_TYPE_SINGLE = "single"
OBJ_CONTAINER_TYPE_LIST = "list"
OBJ_CONTAINER_TYPE_TREE = "tree" # TODO
OBJ_MAX_DEEP_NUM = 3

class Color:
    _GREEN = "\033[92m"
    _RED = "\033[91m"
    _BOLD = '\033[1m'
    _ENDC = '\033[0m'

    @staticmethod
    def red(txt):
        return "%s%s%s%s" % (Color._BOLD, Color._RED, txt, Color._ENDC)

    @staticmethod
    def green(txt):
        return "%s%s%s%s" % (Color._BOLD, Color._GREEN, txt, Color._ENDC)

def set_version(ver):
    global M2C_VERSION
    M2C_VERSION = ver
