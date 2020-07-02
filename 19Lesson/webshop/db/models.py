import mongoengine as me
import datetime


me.connect('webshop')


class Category(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self', default=None)

    def add_subcategory(self, category: 'Category'):
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()

    def get_products(self):
        return Products.objects(category=self)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @property
    def is_parent(self) -> bool:
        return bool(self.subcategories)

    @property
    def is_subcategory(self) -> bool:
        return bool(self.parent)


class ProductAttributes(me.EmbeddedDocument):

    weight = me.IntField()
    width = me.IntField()
    depth = me.IntField()
    height = me.IntField()


class Products(me.Document):
    attributes = me.EmbeddedDocumentField(ProductAttributes)
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.now())
    price = me.DecimalField(required=True)
    in_stock = me.BooleanField(default=True)
    discount = me.IntField(min_value=0, max_value=100)
    image = me.FileField(required=True)
    category = me.ReferenceField('Category')

    def get_discount_price(self):
        return self.price - (self.price/100 * self.discount)


class Text(me.Document):
    TITLES = {
        "greetings": "Текст приветствия",  # ключ - то значение, по которому мы будем обращаться к тайтлам из кода .
        "cart": "Текст корзины",  # Значение - заголовок, который будет храниться в бд.
        "discount1": "Скидка для главного меню",
        "dicsount2": "Скидка для второстепенного меню"

    }

    title = me.StringField(min_length=1, max_length=256, choices=TITLES.values(), unique=True)
    body = me.StringField(min_length=1, max_length=4096)


class Status(me.Document):
    user_status = me.IntField(required=True)
    user_chat_id = me.StringField(required=True, unique=True)


class TempData(me.Document):
    status = me.ReferenceField(Status, unique=True)

    temp_fname = me.StringField(max_length=256)
    temp_phonenumber = me.StringField(max_length=256)
    temp_email = me.StringField(max_length=256)
    temp_address = me.StringField(max_length=256)
    temp_comments = me.StringField(max_length=4096)


class Users(me.Document):

    status = me.ReferenceField(Status, unique=True)

    fname = me.StringField(min_length=2, max_length=256)
    phonenumber = me.StringField(max_length=256)
    email = me.StringField(max_length=256)
    address = me.StringField(max_length=256)
    comments = me.StringField(max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.utcnow())
    total_summ = me.DecimalField(required=True)


class Admin(me.Document):

    username = me.StringField(min_length=2, max_length=15)
    password = me.StringField(min_length=2, max_length=256)


class MyCart(me.Document):
    user = me.ReferenceField(TempData)
    product = me.ReferenceField(Products)
    quantity = me.IntField(required=True)
