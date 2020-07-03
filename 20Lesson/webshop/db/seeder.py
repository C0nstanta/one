from models import (
    Products,
    Category,
    ProductAttributes,
    Text,
    Status,
    Users,
    Admin
)

import os
from os import listdir
from os.path import isfile, join
import random


class RandomSeeder:

    path = os.getcwd()
    image_path = path + "/images/"
    file_path = path + "/random_files/"

    title_list = []
    title_desc_list = []
    category_list = []  # Категории, которые мы можем сидить

    category_db_list = ['tech', 'tech for home', 'items', 'IPhones', 'LG', 'Samsung', 'Laptop',
                        'Scanners', 'TV', 'Cameras']
    # в базе, заносим руками, так как есть нюансы.....

    cat_desc_list = []
    images_list = []

    def product_features_list(self):
        self.images_list = [join(self.image_path, img_file) for img_file in listdir(self.image_path) if
                            isfile(join(self.image_path, img_file))]

        with open(join(self.file_path, "product_name.txt")) as title_file, \
            open(join(self.file_path, "product_description.txt")) as desc_file, \
            open(join(self.file_path, "category_name.txt")) as category_file, \
            open(join(self.file_path, "category_description.txt")) as cat_desc_file:
            self.title_list = [title.rstrip() for title in title_file if title.strip() != ""]
            self.title_desc_list = [title_desc.rstrip() for title_desc in desc_file if title_desc.strip() != ""]
            self.category_list = [category.rstrip() for category in category_file if category.strip() != ""]
            self.cat_desc_list = [cat_desc.rstrip() for cat_desc in cat_desc_file if cat_desc.strip() != ""]

    @staticmethod
    def seed_categories():
        category_titles = ['tech', 'tech for home', 'items']
        category_description = ['here gonna be tech', '...', '...']

        for title, description in zip(category_titles, category_description):
            Category.objects.create(title=title, description=description)

        category_parent = ["Phones", "Computers", "Consumer Electronics"]
        parent_description = ["phones category", "computers category", "home electronic"]
        for title, description in zip(category_parent, parent_description):
            Category.objects.create(title=title, description=description)

        parent = Category.objects.get(title="Phones")
        phone_child = Category.objects.create(title="IPhones", description="6+ and more", parent=parent)
        phone_child1 = Category.objects.create(title="LG", description="4+ and more", parent=parent)
        phone_child2 = Category.objects.create(title="Samsung", description="4+ samsung", parent=parent)
        Category.objects.get(title="Phones").update(subcategories=[phone_child, phone_child1, phone_child2])

        parent = Category.objects.get(title="Computers")
        comp_child1 = Category.objects.create(title="Laptop", description="all lattops here", parent=parent)
        comp_child2 = Category.objects.create(title="Scanners", description="all scanners here", parent=parent)
        Category.objects.get(title="Computers").update(subcategories=[comp_child1, comp_child2])

        parent = Category.objects.get(title="Consumer Electronics")
        electro_chid1 = Category.objects.create(title="TV", description="all tv here", parent=parent)
        electro_chid2 = Category.objects.create(title="Cameras", description="all video here", parent=parent)
        Category.objects.get(title="Consumer Electronics").update(subcategories=[electro_chid1, electro_chid2])

    def seed_products(self, quantity):
        self.product_features_list()
        i = 0
        while i < quantity:
            weight = random.randint(1, 100)
            width = random.randint(1, 100)
            depth = random.randint(1, 100)
            height = random.randint(1, 100)

            title = random.choice(self.title_list)
            description = random.choice(self.title_desc_list)
            price = float(random.randint(500, 3000))
            discount = random.randint(0, 80)
            image_name = random.choice(self.images_list)
            category = Category.objects(title=random.choice(self.category_db_list))[0]
            product = Products(title=title, description=description, price=price, discount=discount, category=category,
                               attributes=ProductAttributes(weight=weight, width=width, depth=depth, height=height))

            with open(image_name, 'rb') as image_file:
                product.image.put(image_file, content_type='image/jpeg')
                product.save()

            i += 1

    @staticmethod
    def init_texts():
        Text.objects.create(title=Text.TITLES['greetings'], body='Рады приветствовать вас в нашем магазине')
        Text.objects.create(title=Text.TITLES['cart'], body='Вы перешли в корзину')

    @staticmethod
    def init_test_user():
        status = Status.objects.create(user_status=3, user_chat_id='11111test11111')

        Users.objects.create(
            status=status,
            fname="FirstBuyerName",
            phonenumber="testphonenumber",
            email="testemail@email.com",
            address="Some address here 9a",
            comments="This is a test user bot",
            total_summ=445.33
        )

    @staticmethod
    def init_admin():
        Admin.objects.create(username="admin", password="123")




if __name__ == "__main__":
    RandomSeeder.init_texts()
    RandomSeeder.init_test_user()
    RandomSeeder.init_admin()
    RandomSeeder.seed_categories()
    RandomSeeder().seed_products(30)

