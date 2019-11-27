from . import create_app
from flask import Flask
from flask.json import JSONEncoder

from bson import json_util

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): return json_util.default(obj)

app = create_app()
app.json_encoder = CustomJSONEncoder

