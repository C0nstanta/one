from marshmallow import Schema, fields, ValidationError, validate


class BlogSchema(Schema):

    auth_name = fields.String(required=True, validate=validate.Length(min=2))
    auth_surname = fields.String(required=True)
    tag_body = fields.List(fields.String())
    header = fields.String(required=True, validate=validate.Length(min=2))
    body = fields.String()