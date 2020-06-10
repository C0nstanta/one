import os
import random
from models import *


class DBManager:

    script_path = os.getcwd()
    file_path = script_path + '/randombase/'

    product_name_list = []
    product_description_list = []
    category_name_list = []
    category_description_list = []

    def seed_categories(self, num_seed=1):
        with open(self.file_path + 'category_name.txt', encoding='utf-8', mode='r') as cat_name:
            for name in cat_name:
                self.category_name_list.append(name.replace('\n', ''))

        with open(self.file_path + 'category_description.txt', encoding='utf-8', mode='r') as cat_descript:
            for name in cat_descript:
                self.category_description_list.append(name.replace('\n', ''))
        i = 0
        while i < num_seed:
            catname_rand = random.choice(self.category_name_list)
            discript_rand = random.choice(self.category_description_list)
            category = Category.objects.create(cat_name=f'{catname_rand}', description=f'{discript_rand}')
            print(f'Category_id:{category.id}, name:{catname_rand}  was added')
            i += 1

    def seed_goods(self, num_seed=1):
        with open(self.file_path + 'product_name.txt', encoding='utf-8', mode='r') as prod_name:
            for name in prod_name:
                self.product_name_list.append(name.replace('\n', ''))

        with open(self.file_path + 'product_description.txt', encoding='utf-8', mode='r') as prod_descript:
            for name in prod_descript:
                self.product_description_list.append(name.replace('\n', ''))
        i = 0
        while i < num_seed:
            category_list = []
            for cat_name in Category.objects:
                category_list.append(cat_name.id)

            catname_rand = random.choice(category_list)
            discript_rand = random.choice(self.product_description_list)
            prod_name_rand = random.choice(self.product_name_list)
            price_rand = random.randint(10, 1000)
            quant_rand = random.randint(1, 10)

            product = Goods.objects.create(name=prod_name_rand, price=price_rand, quantity=quant_rand,
                                           category=catname_rand, product_description=discript_rand)

            print(f'Product_id:{product.id}, name:{product.name}  was added')
            i += 1