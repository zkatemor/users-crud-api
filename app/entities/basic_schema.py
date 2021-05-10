from flask import jsonify
from marshmallow import Schema, fields


class BasicSchema:
    def __init__(self, result=None, error=None, status_code=200):
        self.result = result
        self.error = error
        self.message = 'success' if error is None else error.message
        self.status_code = status_code

    def make_response(self, schema):
        response = jsonify(schema)
        response.status_code = self.status_code
        return response


class BasicResponseSchema(Schema):
    message = fields.String()
    result = fields.Raw()
