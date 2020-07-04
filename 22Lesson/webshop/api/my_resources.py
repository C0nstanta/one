from flask.views import MethodView
from ..db.models import (
    Category,
    ProductAttributes,
    Products,
    Status,
    TempData,
    Users,
    Admin
    )

from ..db.schemas import (
    CategorySchema,
    ProductsSchema,
    StatusSchema,
    TempDataSchema,
    UsersSchema,
    AdminSchema
    )


from flask import request
import random
import os

from marshmallow import ValidationError
import json


class CategoryResource(MethodView):

    @staticmethod
    def get(id_key=None):
        if id_key:
            for category in Category.objects(id=id_key):
                print(f'category.id:{category.id}, category.title:{category.title}')
                return CategorySchema().dumps(category, ensure_ascii=False, default=str)
        else:
            cat_dict = {}
            for category in Category.objects():
                print(f'category.id:{category.id:}, category.title:{category.title}')
                cat_dict[str(category.id)] = category.title
            return CategorySchema(many=True).dumps(Category.objects().all())

    @staticmethod
    def post():
        data = CategorySchema().loads(json.dumps(request.json))
        try:
            if data['title'] and data['description']:
                if data.get('subcategories'):
                    Category.objects.create(title=data['title'], description=data['description'],
                                            subcategories=list(data['subcategories']))
                if data.get('parent'):
                    parent = Category.objects.get(id=data['parent'])
                    Category.objects.create(title=data['title'], description=data['description'],
                                            parent=parent)
                if data.get('subcategories') and data.get('parent'):
                    parent = Category.objects.get(id=data['parent'])
                    Category.objects.create(title=data['title'], description=data['description'],
                                            subcategories=list(data['subcategories']), parent=parent)

                else:
                    Category.objects.create(title=data['title'], description=data['description'])

        except ValidationError as e:
            return e.messages
        return data

    @staticmethod
    def put(id_key=None):
        data = CategorySchema().loads(json.dumps(request.json))
        try:
            changes_list = []
            if data.get('title'):
                Category.objects(id=id_key).update_one(set__title=data['title'])
                changes_list.append(f'title:{data["title"]} changed.')
            if data.get('description'):
                Category.objects(id=id_key).update_one(set__description=data['description'])
                changes_list.append(f'description:{data["description"]} changed.')
        except ValidationError as e:
            return f"{e.messages}:Wrong data dictionary"
        return changes_list

    @staticmethod
    def delete(id_key=None):
        for category in Category.objects(id=id_key):
            category.delete()
            print(f'category.id:{category.id} was deleted.')
            return CategorySchema().dumps(category)


class ProductResource(MethodView):

    path = os.getcwd()
    image_path = path + "/webshop/db/images/"

    @staticmethod
    def get(id_key=None):
        if id_key:
            for product in Products.objects(id=id_key):
                print(f'product.id:{product.id}, product.title:{product.title}')
                return ProductsSchema().dumps(product, ensure_ascii=False, default=str)
        else:
            product_dict = {}
            for product in Products.objects():
                print(f'product.id:{product.id:}, product.title:{product.title}')
                product_dict[str(product.id)] = product.title
            return ProductsSchema(many=True).dumps(Products.objects().all(), ensure_ascii=False, default=str)

    def post(self):
        data = ProductsSchema().loads(json.dumps(request.json, ensure_ascii=False, default=str))
        try:
            if data.get('title') and data.get('description') and data.get('price') and data.get('discount') and \
                    data.get('category'):
                weight = random.randint(1, 100)
                width = random.randint(1, 100)
                depth = random.randint(1, 100)
                height = random.randint(1, 100)

                category = Category.objects.get(id=data.get('category'))
                image_name = self.image_path+"3.jpg"

                product = Products(title=data.get('title'), description=data.get('description'),
                                   price=data.get('price'), discount=data.get('discount'),
                                   category=category, attributes=ProductAttributes(weight=weight, width=width,
                                   depth=depth, height=height))

                with open(image_name, 'rb') as image_file:
                    product.image.put(image_file, content_type='image/jpeg')
                    product.save()

        except ValidationError as e:
            return e.messages
        return data

    @staticmethod
    def put(id_key=None):
        data = ProductsSchema().loads(json.dumps(request.json))
        try:
            changes_list = []
            if data.get('title'):
                Products.objects(id=id_key).update_one(set__title=data['title'])
                changes_list.append(f'title:{data["title"]} changed.')
            if data.get('description'):
                Products.objects(id=id_key).update_one(set__description=data['description'])
                changes_list.append(f'description:{data["description"]} changed.')
            if data.get('price'):
                Products.objects(id=id_key).update_one(set__price=data['price'])
                changes_list.append(f'price:{data["price"]} changed.')
            if data.get('in_stock'):
                Products.objects(id=id_key).update_one(set__in_stock=data['in_stock'])
                changes_list.append(f'in_stock:{data["in_stock"]} changed.')
            if data.get('discount'):
                Products.objects(id=id_key).update_one(set__discount=data['discount'])
                changes_list.append(f'discount:{data["discount"]} changed.')
        except ValidationError as e:
            return f"{e.messages}:Wrong data dictionary"
        return changes_list

    @staticmethod
    def delete(id_key=None):
        for product in Products.objects(id=id_key):
            product.delete()
            print(f'product.id:{product.id} was deleted.')
            return ProductsSchema().dumps(product)


class TempDataResource(MethodView):
    """ В этом классе реализовано только два метода, get и delete.
    Связанно это с тем, что колелкция временная и нам она особо не интересно, посмотреть и удалить достаточно"""
    @staticmethod
    def get(id_key=None):
        if id_key:
            for temp in TempData.objects(id=id_key):
                print(f'temp.id:{temp.id}, temp.temp_phonenumber:{temp.temp_phonenumber}')
                return TempDataSchema().dumps(temp, ensure_ascii=False, default=str)
        else:
            temp_dict = {}
            for temp in TempData.objects():
                print(f'temp.id:{temp.id:}, product.title:{temp.temp_phonenumber}')
                temp_dict[str(temp.id)] = temp.temp_phonenumber
            return TempDataSchema(many=True).dumps(TempData.objects().all(), ensure_ascii=False, default=str)

    @staticmethod
    def delete(id_key=None):
        for temp in TempData.objects(id=id_key):
            temp.delete()
            print(f'tempdata.id:{temp.id} was deleted.')
            return TempDataSchema().dumps(temp)


class UsersResource(MethodView):

    @staticmethod
    def get(id_key=None):
        if id_key:
            for user in Users.objects(id=id_key):
                print(f'user.id:{user.id}, user.fname:{user.fname}, user.phonenumber:{user.phonenumber}')
                return UsersSchema().dumps(user, ensure_ascii=False, default=str)
        else:
            users_dict = {}
            for user in Users.objects():
                print(f'user.id:{user.id:}, user.fname:{user.fname}')
                users_dict[str(user.id)] = [user.fname, user.phonenumber]
            return UsersSchema(many=True).dumps(Users.objects().all(), ensure_ascii=False, default=str)

    @staticmethod
    def post():
        data = UsersSchema().loads(json.dumps(request.json, ensure_ascii=False, default=str))
        try:
            if data.get('fname') and data.get('phonenumber') and data.get('total_summ') and data.get('status'):
                Users.objects.create(**data)

        except ValidationError as e:
            return e.messages
        return data

    @staticmethod
    def put(id_key=None):
        data = UsersSchema().loads(json.dumps(request.json))
        try:
            changes_list = []
            if data.get('fname'):
                Users.objects(id=id_key).update_one(set__fname=data['fname'])
                changes_list.append(f'fname:{data["fname"]} changed.')
            if data.get('phonenumber'):
                Users.objects(id=id_key).update_one(set__phonenumber=data['phonenumber'])
                changes_list.append(f'phonenumber:{data["phonenumber"]} changed.')
            if data.get('total_summ'):
                Users.objects(id=id_key).update_one(set__total_summ=data['total_summ'])
                changes_list.append(f'total_summ:{data["total_summ"]} changed.')
            if data.get('address'):
                Users.objects(id=id_key).update_one(set__address=data['address'])
                changes_list.append(f'address:{data["address"]} changed.')
            if data.get('email'):
                Users.objects(id=id_key).update_one(set__email=data['email'])
                changes_list.append(f'email:{data["email"]} changed.')
        except ValidationError as e:
            return f"{e.messages}:Wrong data dictionary"
        return changes_list

    @staticmethod
    def delete(id_key=None):
        for user in Users.objects(id=id_key):
            user.delete()
            print(f'user.id:{user.id} was deleted.')
            return UsersSchema().dumps(user)


class AdminResource(MethodView):

    @staticmethod
    def get(id_key=None):
        if id_key:
            for admin in Admin.objects(id=id_key):
                print(f'admin.id:{admin.id}, admin.username:{admin.username}, admin.password:{admin.password}')
                return AdminSchema().dumps(admin)
        else:
            admin_dict = {}
            for admin in Admin.objects():
                admin_dict[str(admin.id)] = [admin.username, admin.password]
            print(admin_dict)
            return AdminSchema(many=True).dumps(Admin.objects().all(), ensure_ascii=False, default=str)

    @staticmethod
    def post():
        data = AdminSchema().loads(json.dumps(request.json, ensure_ascii=False, default=str))
        try:
            if data.get('username') and data.get('password'):
                Admin.objects.create(**data)

        except ValidationError as e:
            return e.messages
        return data

    @staticmethod
    def put(id_key=None):
        data = AdminSchema().loads(json.dumps(request.json))
        try:
            changes_list = []
            if data.get('username'):
                Admin.objects(id=id_key).update_one(set__username=data['username'])
                changes_list.append(f'username:{data["username"]} changed.')
            if data.get('password'):
                Admin.objects(id=id_key).update_one(set__password=data['password'])
                changes_list.append(f'password:{data["password"]} changed.')

        except ValidationError as e:
            return f"{e.messages}:Wrong data dictionary"
        return changes_list

    @staticmethod
    def delete(id_key=None):
        for admin in Admin.objects(id=id_key):
            admin.delete()
            print(f'admin.id:{admin.id} was deleted.')
            return AdminSchema().dumps(admin)


class StatusResource(MethodView):

    @staticmethod
    def get(id_key=None):
        if id_key:
            for status in Status.objects(id=id_key):
                print(f'status.id:{status.id}, status.user_chat_id:{status.user_chat_id}, '
                      f'status.user_status:{status.user_status}')
                return StatusSchema().dumps(status)
        else:
            status_dict = {}
            for status in Status.objects():
                status_dict[str(status.id)] = [status.user_chat_id, status.user_status]
            print(status_dict)
            return StatusSchema(many=True).dumps(Status.objects().all(), ensure_ascii=False, default=str)

    @staticmethod
    def post():
        data = StatusSchema().loads(json.dumps(request.json, ensure_ascii=False, default=str))
        try:
            if data.get('user_status') and data.get('user_chat_id'):
                Status.objects.create(**data)

        except ValidationError as e:
            return e.messages
        return data

    @staticmethod
    def put(id_key=None):
        data = StatusSchema().loads(json.dumps(request.json))
        try:
            changes_list = []
            if data.get('user_status'):
                Status.objects(id=id_key).update_one(set__user_status=data['user_status'])
                changes_list.append(f'user_status:{data["user_status"]} changed.')
            if data.get('user_chat_id'):
                Status.objects(id=id_key).update_one(set__user_chat_id=data['user_chat_id'])
                changes_list.append(f'user_chat_id:{data["user_chat_id"]} changed.')

        except ValidationError as e:
            return f"{e.messages}:Wrong data dictionary"
        return changes_list

    @staticmethod
    def delete(id_key=None):
        for status in Status.objects(id=id_key):
            status.delete()
            print(f'status.id:{status.id} was deleted.')
            return StatusSchema().dumps(status)
