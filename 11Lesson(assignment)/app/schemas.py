from marshmallow import Schema, fields, ValidationError, validate


class TeleSchema(Schema):

    fname = fields.String(required=True, validate=validate.Length(min=2))
    mname = fields.String(required=True, validate=validate.Length(min=2))
    sname = fields.String(required=True, validate=validate.Length(min=2))
    phonenumber = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    address = fields.String(required=True, validate=validate.Length(min=2))
    comments = fields.String(required=True, validate=validate.Length(min=2))