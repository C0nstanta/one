from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# модуль, который внутри себя будет держать константы кнопок.
# Ключ - значение, с которым мы будем взаимодействовать в коде. Значение - то,что будет видеть пользователь.
START_KB = {
        'discount_products': 'Товары со скидкой',
        'my_cart': 'Моя корзина',
        'categories': 'Категории',
        'settings': 'Настройки',
        'help': 'Помощь',
        'search': 'Поиск товара'
}

SETTINGS_KB = {
        'name': 'Имя',
        'phone': 'Моб.',
        'address': 'Адрес',
        'email': 'email',
        'home': 'На главную'
}

HOME_BACK_KB = {
        'back': 'Назад',
        'home': 'На главную'
}

HOME_CART_KB = {
    'my_cart': 'Моя корзина',
    'home': 'На главную'
}

ORDER_CART_KB = {
    'order': 'Оформить заказ',
    'del_cart': 'Очистить корзину',
    'home': 'На главную'
}

ORDER_KB = {
    'name': 'Имя',
    'phone': 'Моб.',
    'address': 'Адрес',
    'email': 'email',
    'lets_go': 'Все верно. Оформляем',
    'home': 'На главную'
}

CATEGORY_KB = {
        'categories': 'Категории',
        'home': 'На главную'
}


class KeyBoardShop:

    prev_kb = None

    def start_kb(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)  # , one_time_keyboard=True
        kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
        return kb

    def settings_kb(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # , one_time_keyboard=True
        kb.add(*[KeyboardButton(text=text) for text in SETTINGS_KB.values()])
        return kb

    def go_back_kb(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # , one_time_keyboard=True
        kb.add(*[KeyboardButton(text=text) for text in HOME_BACK_KB.values()])
        return kb

    def home_cart_kb(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # , one_time_keyboard=True
        kb.add(*[KeyboardButton(text=text) for text in HOME_CART_KB.values()])
        return kb

    def order_cart_kb(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # , one_time_keyboard=True
        kb.add(*[KeyboardButton(text=text) for text in ORDER_CART_KB.values()])
        return kb

    def order_kb(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(*[KeyboardButton(text=text) for text in ORDER_KB.values()])
        return kb

    def go_to_category(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(*[KeyboardButton(text=text) for text in CATEGORY_KB.values()])
        return kb

    def set_prev_kb(self, prev_kb):
        self.prev_kb = prev_kb

    def get_prev_kb(self):
        print(self.prev_kb)
        return self.prev_kb
