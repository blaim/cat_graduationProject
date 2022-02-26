__all__ = ['testing']

# Don't look below, you will not understand this Python code :) I don't.
from js2py import require
from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['jsonData'])
var.put('jsonData', var.get('require')(Js('../json/data.json')))
var.get('console').callprop('log', var.get('jsonData'))
pass


# Add lib to the module scope
testing = var.to_python()