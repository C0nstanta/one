
from flask.views import MethodView
from models import Goods, Category
from flask import jsonify, request
from schemas import ShopSchema
from marshmallow import ValidationError
import re
import json


class ShopResource(MethodView):

    @staticmethod
    def get(id_key=None):
        if id_key:
            try:
                for product in Goods.objects(id=id_key):
                    print(f'product.id:{product.id}, product.name:{product.name}')
                    Goods.objects(id=id_key).update_one(inc__views=1)
                    return ShopSchema().dumps(product)
            except ValidationError as e:
                return e.messages
        else:
            for product in Goods.objects():
                category_obj = product['category']
                print(category_obj.id, category_obj.cat_name, category_obj.description)
                print(f'product.id:{product.id}, product.price:{product.price}, product.views:{product.views}')
            return ShopSchema(many=True).dumps(Goods.objects().all())

    @staticmethod
    def post():
        data = ShopSchema().loads(json.dumps(request.json))
        try:
            if data['name'] and data['price'] and data['quantity'] and data['category_name']:
                print("good")
                if Category.objects(cat_name=data['category_name']):
                        print('This category already exists.')

                        category_id = [cat.id for cat in Category.objects(cat_name=data['category_name'])]
                        Goods.objects.create(name=data['name'], price=data['price'], quantity=data['quantity'],
                                             category=category_id, product_description=data.get('prod_desc'))
                else:
                    print('New category. Create it first.')
                    category = Category.objects.create(cat_name=data['category_name'],
                                                       description=data.get('cat_description'))
                    Goods.objects.create(name=data['name'], price=data['price'], quantity=data['quantity'],
                                               category=category.id, product_description=data.get('prod_desc'))
        except ValidationError as e:
            return e.messages
        return data

    @staticmethod
    def put(id_key=None):
        data = ShopSchema().loads(json.dumps(request.json))
        print(data)
        try:
            Goods.objects(id=id_key).update(**data)
        except ValidationError as e:
            return e.messages
        return data

    @staticmethod
    def delete(id_key=None):
        for product in Goods.objects(id=id_key):
            product.delete()
            return f'product.id:{product.id} was deleted.'


class TotalSum(MethodView):

    @staticmethod
    def get():
        total = Goods.objects.sum('price')
        return total