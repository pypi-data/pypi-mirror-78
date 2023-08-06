
#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2019.07.20

class SwaggerSchema(object):
    def __init__(self, name, type, ref, description):
        self.name = name
        self.type = type # array / object
        self.ref = ref
        self.description = description

        self.required = [] # param_name in properties
        self.properties = {} # param_name : propertie
        self.items = None # type array's item schema

    def addRequiredParam(self, name):
        self.required.append(name)

    def addPropertieItem(self, name, schema):
        assert isinstance(schema, SwaggerSchema)
        self.properties[name] = schema

    def setArrayItem(self, schema):
        assert isinstance(schema, SwaggerSchema)
        self.type = 'array'
        self.items = schema

    def todict(self):
        d = {'type': self.type, 'description': self.description}
        if self.ref:
            d['$ref'] = self.ref
        elif self.items:
            d['items'] = self.items.todict()

        if len(self.required) > 0:
            d['required'] = self.required

        dp = {}
        for k, v in self.properties.items(): # py2 vs py3
            dp[k] = v.todict()
        if len(dp) > 0:
            d['properties'] = dp

        return d
