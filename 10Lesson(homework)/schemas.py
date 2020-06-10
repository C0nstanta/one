from marshmallow import Schema, fields, ValidationError, validate


class ShopSchema(Schema):

    name = fields.String(required=True, validate=validate.Length(min=2))
    product_description = fields.String(required=True, validate=validate.Length(min=2, max=4096))
    price = fields.Float(validate=validate.Range(min=0, max=None))
    quantity = fields.Integer(validate=validate.Range(min=0, max=None))
    description = fields.String(validate=validate.Length(max=4096))
    cat_name = fields.String(required=True, validate=validate.Length(min=2))
    category = fields.String(required=True)