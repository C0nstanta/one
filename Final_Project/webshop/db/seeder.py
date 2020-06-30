from models import Products, Category, ProductAttributes
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

    category_db_list = ['5eefb7fbfe2eea772a570105', '5eefb7fbfe2eea772a570106', '5eefb7fbfe2eea772a570107']
    # ["5ef08eb6ca2aadc0585df8d2", "5ef0876aca2aadc0585df8d1"]  # Категории, которые уже есть
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
            category = Category.objects(id=random.choice(self.category_db_list))[0]
            product = Products(title=title, description=description, price=price, discount=discount, category=category,
                               attributes=ProductAttributes(weight=weight, width=width, depth=depth, height=height))

            with open(image_name, 'rb') as image_file:
                product.image.put(image_file, content_type='image/jpeg')
                product.save()

            i += 1


if __name__ == "__main__":
#    RandomSeeder().seed_products(1)
       RandomSeeder.seed_categories()
