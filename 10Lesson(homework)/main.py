# TODO:
# 1) Реализовать REST интернет магазина. Модель товар (цена,
# доступность, кол-во доступных единиц, категория, кол-во просмотров),
# Категория (описание, название). При обращении к конкретному товару
# увеличивать кол-во просмотров на 1. Добавить модуль для заполнения
# БД валидными данными. Реализовать подкатегории ( доп. Бал). Добавить
# роут, который выводят общую стоимость товаров в магазине.
"""
/shop/all - вывод товара в одну кучу
/shop/get/<string:id_key> - вывод товара по ключу. при выводе увеличивается количество просмотров.
/shop/delete/<string:id_key> - удаление товара по ключу
/shop/update/<string:id_key> - обновление данных по указанному id
/shop/totalsum - вывод общей  стоимости товара.

Генерация товара просиходит в файле main путем добавления требуемого метода.
    dbmanager = DBManager()
    dbmanager.seed_categories(1)
    dbmanager.seed_goods(1)

"""

from flask import Flask
from flask_restful import Api
from my_resources import ShopResource, TotalSum

app = Flask(__name__)
api = Api(app)

api.add_resource(ShopResource, '/shop/all', endpoint='get_all', methods=['GET'])
api.add_resource(ShopResource, '/shop/get/<string:id_key>', endpoint='get_by_id', methods=['GET'])
api.add_resource(ShopResource, '/shop/add', endpoint='post', methods=['POST'])
api.add_resource(ShopResource, '/shop/update/<string:id_key>', endpoint='put', methods=['PUT'])
api.add_resource(ShopResource, '/shop/delete/<string:id_key>', endpoint='delete', methods=['DELETE'])
api.add_resource(TotalSum, '/shop/totalsum', endpoint='summ', methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
