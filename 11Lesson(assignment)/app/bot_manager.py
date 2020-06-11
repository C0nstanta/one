import random
from .models import Users
from .schemas import TeleSchema
from marshmallow import ValidationError
import re
import json

class DBManager:

    user_dict = {}

    def get_fio(self, fio_str):
        pattern = '\w+'
        fio = re.findall(pattern, fio_str)
        try:
        #if fio[0] and fio[1] and fio[2]:
            self.user_dict['fname'] = str(fio[0])
            self.user_dict['mname'] = str(fio[1])
            self.user_dict['sname'] = str(fio[2])
            return True
        except IndexError as e:
            print(e)
        return False

    def get_phone(self, num):
        pattern = '\d+'
        phone = re.findall(pattern, num)
        try:
            self.user_dict['phonenumber'] = str(phone[0])
            return True
        except IndexError as e:
            print(e)
        return False

    def get_email(self, email_raw):
        pattern = '[\w\-_\..]+@[\w]+.[\w]{2,3}'
        try:
            email = re.findall(pattern, email_raw)
            self.user_dict['email'] = str(email[0])
            return True
        except IndexError as e:
            print(e)
        return False

    def get_address(self, address_raw):
        try:
            self.user_dict['address'] = str(address_raw)
            return True
        except IndexError as e:
            print(e)
        return False

    def get_comment(self,raw_comment):
        try:
            self.user_dict['comments'] = str(raw_comment)
            self.write_to_db()
            return True
        except IndexError as e:
            print(e)
        return False

    def write_to_db(self):
        data = TeleSchema().loads(json.dumps(self.user_dict))
        print(data)
        try:
            Users.objects.create(**data)
        except ValidationError as e:
            print(e)





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