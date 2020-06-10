"""Модель товар (цена,
# доступность, кол-во доступных единиц, категория, кол-во просмотров),
# Категория (описание, название). При обращении к конкретному товару
# увеличивать кол-во просмотров на 1. """


import mongoengine as me
import datetime
from seeder_lib import *

me.connect('EShop')


class Category(me.Document):

    description = me.StringField(max_length=4096)
    cat_name = me.StringField(min_length=2, max_length=256)


class Goods(me.Document):

    name = me.StringField(min_length=2, max_length=256)
    price = me.DecimalField(min_value=0)
    in_stock = me.BooleanField(default=True)
    quantity = me.IntField(min_value=0)
    category = me.ReferenceField(Category)
    views = me.IntField(min_value=0)
    created = me.DateTimeField(default=datetime.datetime.utcnow())
    product_description = me.StringField(max_length=4096)


if __name__ == "__main__":

    dbmanager = DBManager()
#    dbmanager.seed_categories(5)
    dbmanager.seed_goods(12)


#category = Category.objects.create(description="Some description here", cat_name="Refrigerators")

#    goods = Goods.objects.create(name="Refrigerator Nord", price=100, in_stock=True, quantity=1, category=category, views=0)

# auth_id_rand = random.choice(list(self.author_dict))
# tag_rand = random.choice(self.tag_list)
# body_text_rand = random.choice(self.body_list)
# title_text_rand = random.choice(self.header_list)
#
# rand_author = Author.objects(id=auth_id_rand).get()
# tag = Tag.objects.create(tag_body=[tag_rand])
# post = Post.objects.create(author=rand_author, header=title_text_rand, body=body_text_rand, views=1,
#                            tag=tag)


#    dbmanager = DBManager()
#    dbmanager.seed_posts(1)  # Это сидер постов( количество которых передаем в метод класса). Сидятся посты и теги
#    # одновременно. Авторы берутся из существующих
#
#    dbmanager.seed_authors(1)  # Это сидер авторов( количество которых передаем в метод класса)


"""

import mongoengine as me
import datetime

me.connect('webshop_adv_april')



#            ТЕХНИКА#root
#               |
#          БЫТОВАЯ ТЕХНИКА#child (подкатегория)
#          /     |       \
#    Холодил.  Микроволн.  Чайник #childs



class Category(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self', default=None)


class Product(me.Document):
    #attrs
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.now())
    price = me.DecimalField(required=True)
    discount = me.IntField(min_value=0, max_value=100)
    in_stock = me.BooleanField(default=True)
    image = me.FileField(required=True)
    category = me.ReferenceField(Category)
"""