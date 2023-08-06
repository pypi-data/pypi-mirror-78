#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2019.07.20

import os
import json
from .apimodel import ApiModel, ApiDef
from .objmodel import ObjModel
from .schema import SwaggerSchema
from .conf import Color, MOD
from .helper import IS_PY3

# OpenAPI Swargger https://swagger.io/specification

SWAGGER_INDEX = '''
<!-- HTML for static distribution bundle build -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.0/swagger-ui.css" >
    <style>
      html
      {
        box-sizing: border-box;
        overflow: -moz-scrollbars-vertical;
        overflow-y: scroll;
      }

      *,
      *:before,
      *:after
      {
        box-sizing: inherit;
      }

      body
      {
        margin:0;
        background: #fafafa;
      }
    </style>
  </head>

  <body>
    <div id="swagger-ui"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.0/swagger-ui-bundle.js"> </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.0/swagger-ui-standalone-preset.js"> </script>
    <script>
    window.onload = function() {
      // Begin Swagger UI call region
      let hash = window.location.hash
      let url = window.location.href
      url = url.replace(hash, '') + '.yaml'
      const ui = SwaggerUIBundle({
        url: url,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout"
      })
      // End Swagger UI call region

      window.ui = ui
    }
  </script>
  </body>
</html>
'''

class SwaggerInformation(object):
    def __init__(self, title, description, version):
        self.title = title
        self.description = description
        self.version = version

    def todict(self):
        return {'title': self.title, 'description': self.description, 'version': self.version}

class SwaggerTag(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def todict(self):
        return {'name': self.name, 'description': self.description}

class SwaggerServer(object):
    def __init__(self, url, description):
        self.url = url
        self.description = description

    def todict(self):
        return {'url': self.url, 'description': self.description}

class SwaggerPathItem(object):
    def __init__(self, path, description, postop=None, getop=None):
        self.path = path
        self.description = description
        self.postop = postop # post operation
        self.getop = getop # get operation

    def setGetOperation(self, op):
        assert isinstance(op, SwaggerOperation)
        self.getop = op

    def setPostOperation(self, op):
        assert isinstance(op, SwaggerOperation)
        self.postop = op

    def todict(self):
        d = {'description': self.description}
        if hasattr(self, 'getop') and self.getop:
            d['get'] = self.getop.todict()
        if hasattr(self, 'postop') and self.postop:
            d['post'] = self.postop.todict()
        return d

class SwaggerOperation(object):
    def __init__(self, summary, description, operationID):
        self.summary = summary # short desc
        self.description = description
        self.operationID = operationID # apiName
        self.tags = [] # apiGroup
        self.parameters = [] # get request in query, ref schema
        self.requestBody = None # post request, ref schema
        self.responses = None

    def addTag(self, tag):
        self.tags.append(tag)

    def addQueryParam(self, param):
        assert isinstance(param, SwaggerParameter)
        self.parameters.append(param)

    def setRequestBodyRef(self, contentType, ref):
        self.requestBody = {
            'content': {
                contentType: {
                    'schema': {'$ref': ref}
                }
            }
        }

    def setResponseRef(self, statusCode, description, contentType, ref):
        self.responses = {
            statusCode: {
                'description': description,
                'content': {
                    contentType: {'schema': {'$ref': ref}}
                }
            }
        }

    def todict(self):
        d = {'summary': self.summary, 'description': self.description, 'operationId': self.operationID}
        if len(self.tags) > 0:
            d['tags'] = self.tags
        if len(self.parameters) > 0:
            d['parameters'] = list(map(lambda x: x.todict(), self.parameters))
        if self.requestBody:
            d['requestBody'] = self.requestBody
        if self.responses:
            d['responses'] = self.responses
        return d

class SwaggerParameter(object):
    def __init__(self, location, name, description, schema, required=True):
        self.location = location
        self.name = name # param_name
        self.description = description
        self.required = required
        self.schema = schema

    def todict(self):
        d = {'in': self.location, 'name': self.name, 'description': self.description, 'required': self.required}
        d['schema'] = self.schema.todict()
        return d

class Swagger(object):
    def __init__(self, title, description, version):
        self.openapi = '3.0.0'
        self.info = SwaggerInformation(title, description, version)
        self.servers = []
        self.paths = {} # apis {"/login", SwaggerItem}
        self.tags = [] # groups
        self.definitions = {} # models, properties_name: properties

    def addServer(self, url, description):
        self.servers.append(SwaggerServer(url, description))

    def addTag(self, name, description):
        self.tags.append(SwaggerTag(name, description))

    def addPath(self, name, sgItem):
        assert isinstance(sgItem, SwaggerPathItem)
        assert name not in self.paths
        self.paths[name] = sgItem

    def addDefinition(self, name, schema):
        assert isinstance(schema, SwaggerSchema)
        assert name not in self.definitions, Color.red('definition "%s" conflict.' % name)
        self.definitions[name] = schema

    def todict(self):
        d = {'openapi': self.openapi}
        dps = {}
        for k, v in self.paths.items():
            dps[k] = v.todict()
        d['paths'] = dps
        dds = {}
        for k, v in self.definitions.items():
            dds[k] = v.todict()
        d['components'] = {'schemas': dds}
        d['tags'] = list(map(lambda x: x.todict(), self.tags))
        d['servers'] = list(map(lambda x: x.todict(), self.servers)) # py2 vs py3
        if self.info:
            d['info'] = self.info.todict()
        return d

def genSwaggerContent():
    lines = open('apimodel.txt', 'rb').readlines()
    if IS_PY3(): # py2 vs py3
        lines = list(map(lambda x: x.decode('utf-8'), lines))
    apiModel = ApiModel.fromLines(lines)

    # sg
    sg = Swagger(apiModel.title, apiModel.description, apiModel.srvVersion)
    sg.addServer(apiModel.apiServer, '')

    for group in apiModel.groups:
        sg.addTag(group.group, group.comment)

        for api in group.apis:
            path = SwaggerPathItem(api.apiName(), api.comment)
            op = SwaggerOperation(api.comment, api.comment, api.apiFullName())
            reqContentType = 'application/json'
            respContentType = 'application/json'
            if api.proto == 'raw':
                reqContentType = 'application/octet-stream'
                respContentType = 'application/octet-stream'
            elif api.proto == 'reqRaw':
                reqContentType = 'application/octet-stream'
            elif api.proto == 'respRaw':
                respContentType = 'application/octet-stream'

            op.addTag(api.group)

            # api req model
            reqModel = SwaggerSchema(api.reqModelName(), 'object', '', api.comment)
            for param in api.apiParams:
                if param.required:
                    reqModel.addRequiredParam(param.name)
                reqModel.addPropertieItem(param.name, param.schema())

                if api.method.lower() == 'get':
                    qpm = SwaggerParameter('query', param.name, param.comment, param.schema(), param.required)
                    op.addQueryParam(qpm)

            if api.method.lower() != 'get':
                sg.addDefinition(api.reqModelName(), reqModel)

            # api resp model
            respModel = SwaggerSchema(api.respModelName(), 'object', '', api.comment)
            for resp in api.apiResps:
                if resp.required:
                    respModel.addRequiredParam(resp.name)
                respModel.addPropertieItem(resp.name, resp.schema())

            sg.addDefinition(api.respModelName(), respModel)

            # request param
            if api.method.lower() != 'get':
                op.setRequestBodyRef(reqContentType, '#/components/schemas/%s' % api.reqModelName())

            # response
            op.setResponseRef(200, api.comment, respContentType, '#/components/schemas/%s' % api.respModelName())

            if api.method.lower() == 'get':
                path.setGetOperation(op)
            else:
                path.setPostOperation(op)

            apiName = '/api/%s/%s/%s' % (apiModel.version, api.group, api.apiRouterName())
            sg.addPath(apiName, path)

    d = sg.todict()
    from yaml import safe_dump
    return safe_dump(d, indent=4)

def genSwaggerYaml(savePath):
    content = genSwaggerContent()
    fp = open(savePath, 'wb')
    header = '# Code generated by m2c. DO NOT EDIT.\n'
    if IS_PY3():
        fp.write(header.encode('utf-8'))
        fp.write(content.encode('utf-8'))
    else:
        fp.write(header)
        fp.write(content)
    fp.close()

def genSwaggerGwGo(savePath):
    content = genSwaggerContent()
    fp = open(savePath, 'wb')
    code = '''
// Code generated by m2c. DO NOT EDIT.
package gw

const SWAGGER_INDEX = `
%s
`

const SWAGGER_CONTENT = `
%s
`
    ''' % (SWAGGER_INDEX, content)
    if IS_PY3():
        fp.write(code.encode('utf-8'))
    else:
        fp.write(code)
    fp.close()
    os.system('gofmt -w %s/' % MOD)

def genSwaggerGwGoV4(savePath):
    content = genSwaggerContent()
    fp = open(savePath, 'wb')
    code = '''
// Code generated by m2c. DO NOT EDIT.
package router

const SWAGGER_INDEX = `
%s
`

const SWAGGER_CONTENT = `
%s
`
    ''' % (SWAGGER_INDEX, content)
    if IS_PY3():
        fp.write(code.encode('utf-8'))
    else:
        fp.write(code)
    fp.close()
    os.system('gofmt -w %s/' % MOD)
