from flask import Flask
from flask_restful import Api
from .bot.main import telegram_bp
from .api.client import auth_bp
from webshop.api.my_resources import (
    CategoryResource,
    ProductResource,
    TempDataResource,
    UsersResource,
    AdminResource,
    StatusResource
    )


app = Flask(__name__)
api = Api(app)


api.add_resource(CategoryResource, '/tg/category/all', '/tg/category/all/<string:id_key>')
api.add_resource(ProductResource, '/tg/products/all', '/tg/products/all/<string:id_key>')
api.add_resource(TempDataResource, '/tg/tempdata/all', '/tg/tempdata/all/<string:id_key>')
api.add_resource(UsersResource, '/tg/users/all', '/tg/users/all/<string:id_key>')
api.add_resource(AdminResource, '/tg/admin/all', '/tg/admin/all/<string:id_key>')
api.add_resource(StatusResource, '/tg/status/all', '/tg/status/all/<string:id_key>')


app.register_blueprint(telegram_bp)
app.register_blueprint(auth_bp)
