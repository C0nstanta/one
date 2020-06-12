from marshmallow import Schema, fields, validate


class StatusSchema(Schema):
    user_status = fields.Integer(required=True, validate=validate.Range(min=0,max=10))
    user_chat_id = fields.String(required=True)


class TeleSchema(Schema):

    fname = fields.String(required=True, validate=validate.Length(min=2))
    mname = fields.String(required=True, validate=validate.Length(min=2))
    sname = fields.String(required=True, validate=validate.Length(min=2))
    phonenumber = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    address = fields.String(required=True, validate=validate.Length(min=2))
    comments = fields.String(required=True, validate=validate.Length(min=2))
    status = fields.Nested(StatusSchema)