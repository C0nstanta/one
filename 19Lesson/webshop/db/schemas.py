from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=2, max=512))
    description = fields.String(required=True, validate=validate.Length(min=2, max=4096))
    parent = fields.String()
    subcategories = fields.List(fields.String())


class ProductAttributesSchema(Schema):

    weight = fields.Int(validate=validate.Length(max=10))
    width = fields.Int(validate=validate.Length(max=10))
    depth = fields.Int(validate=validate.Length(max=10))
    height = fields.Int(validate=validate.Length(max=10))


class ProductsSchema(Schema):

    category = fields.String(required=True)
    title = fields.String(required=True, validate=validate.Length(min=2, max=512))
    description = fields.String(required=True, validate=validate.Length(min=2, max=4096))
    price = fields.Float(required=True)
    in_stock = fields.Bool(required=True)
    discount = fields.Int(required=True, validate=validate.Range(min=0, max=100))


class StatusSchema(Schema):
    user_status = fields.Int(required=True, validate=validate.Range(min=0, max=3))
    user_chat_id = fields.String(required=True, validate=validate.Length(min=1, max=20))


class TempDataSchema(Schema):

    status = fields.String(required=True)
    temp_fname = fields.String(validate=validate.Length(max=256))
    temp_phonenumber = fields.String(validate=validate.Length(min=6, max=13))
    temp_email = fields.String(validate=validate.Email())
    temp_address = fields.String(validate=validate.Length(max=256))
    temp_comments = fields.String(validate=validate.Length(max=4096))


class UsersSchema(Schema):

    status = fields.String(required=True)
    fname = fields.String(required=True, validate=validate.Length(min=2, max=50))
    phonenumber = fields.String(required=True, validate=validate.Length(min=6, max=13))
    email = fields.String(validate=validate.Email())
    address = fields.String(validate=validate.Length(max=256))
    comments = fields.String(validate=validate.Length(max=4096))
    total_summ = fields.Float(required=True, validate=validate.Range(min=1, max=100000000000))


class AdminSchema(Schema):

    username = fields.String(required=True, validate=validate.Length(min=2, max=15))
    password = fields.String(required=True, validate=validate.Length(min=2, max=256))


class MyCartSchema(Schema):

    user = fields.Nested(UsersSchema)
    product = fields.Nested(ProductsSchema)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
