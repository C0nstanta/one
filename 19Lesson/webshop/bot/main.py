from telebot import TeleBot
from flask import Flask, request, abort

from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from .config import TOKEN, WEBHOOK_URL
from ..db.models import Text
from ..db.bot_manager import DBManager
from ..db.models import Category, Products, MyCart
from .keyboards import (
    START_KB,
    SETTINGS_KB,
    HOME_BACK_KB,
    KeyBoardShop,
    ORDER_CART_KB,
    ORDER_KB
)
from .lookups import (
    category_lookup,
    separator,
    add_product,
    del_product,
    min_product,
    go_back
)
import re
import time

bot = TeleBot(TOKEN)
kb_shop = KeyBoardShop()
dbmanager = DBManager()

app = Flask(__name__)


@app.route('/tg', methods=['POST'])
def process_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(status=403)


# Приветствие и проверка зашедшего юзера
@bot.message_handler(commands=['start'])
def start(message):
    status_id = dbmanager.check_status(message.chat.id)
    if status_id == 0:
        bot.send_message(message.chat.id, 'Вы забанены.).')
        return

    if status_id == 1:
        txt = Text.objects.get(title=Text.TITLES['greetings']).body
        kb = kb_shop.start_kb()
        kb_shop.set_prev_kb(kb)
        bot.send_message(message.chat.id, txt, reply_markup=kb)

    if status_id == 2:
        bot.send_message(message.chat.id, 'C возвращением ).')
        txt = Text.objects.get(title=Text.TITLES['greetings']).body
        kb = kb_shop.start_kb()
        kb_shop.set_prev_kb(kb)
        bot.send_message(message.chat.id, txt, reply_markup=kb)


# Описание  reply кнопки 'На главную'
@bot.message_handler(content_types=['text'], func=lambda call: call.text == HOME_BACK_KB['home'])
def hello(message):
    kb = kb_shop.start_kb()
    kb_shop.set_prev_kb(kb)
    bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=kb)


# Описание  reply кнопки 'Назад'
@bot.message_handler(content_types=['text'], func=lambda call: call.text == HOME_BACK_KB['back'])
def back(message):
    kb = kb_shop.get_prev_kb()
    bot.send_message(message.chat.id, "Возврат к предыдущему меню.", reply_markup=kb)


# Описание  reply кнопки 'Товары со скидкой'
@bot.message_handler(content_types=['text'], func=lambda call: call.text == START_KB['discount_products'])
def discount(message):

    kb = kb_shop.go_back_kb()
    bot.send_message(message.chat.id, "Список товаров со скидкой", reply_markup=kb)

    disc_products = [product for product in Products.objects if product.discount != 0]
    for product in disc_products:
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text=f'Добавить в корзину',
                                      callback_data=f'{add_product}{separator}{product.id}')
        kb.add(button)

        bot.send_photo(message.chat.id, product.image.get(), caption=f'<b>Title:{product.title}</b>\n'
            f'<b>Description:</b>{product.description}\n<b>Price:</b><s>{product.price}</s>\n'
            f'<b>Discount price:</b>{product.get_discount_price()}\n<b>Product weight:</b>'
            f'{product.attributes.weight}\n'
            f'<b>Product(WxHxD):</b>{product.attributes.width}x{product.attributes.height}x'
            f'{product.attributes.depth}', parse_mode='HTML', reply_markup=kb)
        time.sleep(1)


# Описание  reply кнопки 'Моя корзина'
@bot.message_handler(content_types=['text'], func=lambda call: call.text == START_KB['my_cart'])
def my_cart(message):

    if dbmanager.check_status(message.chat.id) < 2:
        dbmanager.create_data(message.chat.id, temp_new_name=message.chat.first_name)

    user_id = DBManager.check_my_cart(message.chat.id)
    if user_id:
        bot.send_message(message.chat.id, "У вас в корзине следующие продукты:")
        for cart in MyCart.objects(user=user_id):
            product = Products.objects(id=cart.product.id)[0]

            kb = InlineKeyboardMarkup(row_width=2)
            button_plus = InlineKeyboardButton(text=f'+1', callback_data=f'{add_product}{separator}{product.id}')
            button_min = InlineKeyboardButton(text=f'-1', callback_data=f'{min_product}{separator}{product.id}')
            button_del = InlineKeyboardButton(text=f'Удалить товар из корзины',
                                              callback_data=f'{del_product}{separator}{product.id}')
            kb.add(button_plus, button_min)
            kb.add(button_del)

            bot.send_photo(message.chat.id, product.image.get(), caption=f'<b>Title:{product.title}</b>\n'
            f'<b>Description:</b>{product.description}\n<b>Price:</b><s>{product.price}</s>\n'
            f'<b>Discount price:</b>{product.get_discount_price()}\n<b>Product weight:</b>'
            f'{product.attributes.weight}\n'
            f'<b>Product(WxHxD):</b>{product.attributes.width}x{product.attributes.height}x'
            f'{product.attributes.depth}\n<b>Количество в корзине:</b>{cart.quantity}', parse_mode='HTML',
                           reply_markup=kb)

            time.sleep(1)
        kb_reply = kb_shop.order_cart_kb()
        kb_shop.set_prev_kb(kb_reply)
        total_price = dbmanager.total_cart(message.chat.id)
        if total_price == 0:
            kb_reply = kb_shop.go_to_category()
            bot.send_message(message.chat.id, f'Ваша корзина пуста.', reply_markup=kb_reply)
        else:
            bot.send_message(message.chat.id, f'Total sum in your cart:{total_price}', reply_markup=kb_reply)
    else:
        kb_reply = kb_shop.go_to_category()
        bot.send_message(message.chat.id, f'Вы гость и ваша корзина абсолютно пуста.', reply_markup=kb_reply)


# Описание  reply кнопки 'Оформить заказ'
@bot.message_handler(content_types=['text'], func=lambda call: call.text == ORDER_CART_KB['order'])
def check_order(message):
    kb = kb_shop.order_kb()
    kb_shop.set_prev_kb(kb)
    name, phone, email, address = DBManager.get_user_data(message.chat.id)
    bot.send_message(message.chat.id, f"<b>Реквизиты, на которые делается заказ:</b>\n"
                                      f"<b>Имя:{name}</b>\n<b>Телефон:</b>{phone}\n<b>Email:</b>{email}\n"
                                      f"<b>Адрес:</b>{address}", reply_markup=kb, parse_mode='HTML')


# Описание  reply кнопки 'Оформить заказ' --> "Все верно. Оформляем"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == ORDER_KB['lets_go'])
def check_order(message):
    if dbmanager.check_phone_number(message.chat.id):
        kb = kb_shop.start_kb()
        dbmanager.create_user(message.chat.id)
        bot.send_message(message.chat.id, "Заказ принят, оператор Вам перезвонит в течении 1 минуты.", reply_markup=kb)

    else:
        kb = kb_shop.settings_kb()
        bot.send_message(message.chat.id, "Введите корректно свой контактный телефонный номер.", reply_markup=kb)


# Описание  Inline клавиатуры в меню "Категории"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == START_KB['categories'])
def categories(message):
    kb = InlineKeyboardMarkup()
    roots = Category.get_root_categories()
    buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
               for category in roots]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text='Выберите категорию', reply_markup=kb)


# Описание  Inline клавиатуры в меню "Категории"
@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == category_lookup)
def category_click(call):
    category_id = call.data.split(separator)[1]
    category = Category.objects.get(id=category_id)
    kb = InlineKeyboardMarkup()

    if category.is_parent:
        subcategories = category.subcategories
        buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
                   for category in subcategories]

        kb.add(*buttons)
        bot.edit_message_text(category.title, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=kb)

    else:
        product_list = [product.id for product in category.get_products()]

        for prod_id in product_list:
            bot.send_message(call.message.chat.id, f"Выводим продукты:{prod_id}")
            product = Products.objects(id=prod_id)[0]
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text=f'Добавить в корзину',
                                          callback_data=f'{add_product}{separator}{product.id}')
            kb.add(button)

            bot.send_photo(call.message.chat.id, product.image.get(), caption=f'<b>Title:{product.title}</b>\n'
                f'<b>Description:</b>{product.description}\n<b>Price:</b><s>{product.price}</s>\n'
                f'<b>Discount price:</b>{product.get_discount_price()}\n<b>Product weight:</b>'
                f'{product.attributes.weight}\n'
                f'<b>Product(WxHxD):</b>{product.attributes.width}x{product.attributes.height}x'
                f'{product.attributes.depth}', parse_mode='HTML', reply_markup=kb)
            time.sleep(1)
    kb = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text=f'Назад', callback_data=f'goback_{category.id}')
    kb.add(button)
    kb_reply = kb_shop.home_cart_kb()
    kb_shop.set_prev_kb(kb_reply)
    bot.send_message(call.message.chat.id, "Выберите товар или пункт меню", reply_markup=kb)


# Описание в Inline кнопки "Назад"
@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == go_back)
def category_click(call):
    idx = call.data.split(separator)[1]
    category = Category.objects.get(id=idx)

    if category.is_subcategory:
        parent = category.parent
        sucategories = Category.objects.get(id=parent.id).subcategories
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
                   for category in sucategories]
        kb.add(*buttons)
        bot.send_message(call.message.chat.id, text='Выберите категорию', reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup()
        root = Category.get_root_categories()
        buttons_root = [InlineKeyboardButton(text=category.title,
                        callback_data=f'{category_lookup}{separator}{category.id}') for category in root]

        kb.add(*buttons_root)
        bot.send_message(call.message.chat.id, text='Выберите категорию', reply_markup=kb)


# Описание в Inline кнопки "Добавить" и "+1"
@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == add_product)
def add_to_cart(call):
    if dbmanager.check_status(call.message.chat.id) < 2:
        dbmanager.create_data(call.message.chat.id, temp_new_name=call.message.chat.first_name)

    product_id = call.data.split(separator)[1]
    quantity, title = dbmanager.add_my_cart(product_id, call.message.chat.id)
    bot.send_message(call.message.chat.id, f"<b>Title:</b>{title}\n<b>Quantity in cart:</b>{quantity}",
                     parse_mode='HTML')
    kb = kb_shop.go_back_kb()
    total_price = dbmanager.total_cart(call.message.chat.id)
    bot.send_message(call.message.chat.id, f'Total sum in your cart:{total_price}', reply_markup=kb)


# Описание в Inline кнопки "-1"
@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == min_product)
def min_cart(call):
    product_id = call.data.split(separator)[1]
    quantity, title = DBManager.min_my_cart(product_id, call.message.chat.id)
    bot.send_message(call.message.chat.id, f"<b>Title:</b>{title}\n<b>Quantity in cart:</b>{quantity}",
                     parse_mode='HTML')
    kb = kb_shop.go_back_kb()
    total_price = dbmanager.total_cart(call.message.chat.id)
    bot.send_message(call.message.chat.id, f'Total sum in your cart:{total_price}', reply_markup=kb)


# Описание в Inline кнопки "Удалить продукт"
@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == del_product)
def del_cart_product(call):
    product_id = call.data.split(separator)[1]
    kb = kb_shop.go_back_kb()
    title = DBManager.del_cart_product(product_id, call.message.chat.id)
    total_price = dbmanager.total_cart(call.message.chat.id)

    bot.send_message(call.message.chat.id, f'<b>{title}</b>\n<b>Total sum:</b>{total_price}', parse_mode='HTML',
                     reply_markup=kb)


# Описание в Inline кнопки "Очистить корзину"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == ORDER_CART_KB['del_cart'])
def del_cart(message):
    kb = kb_shop.go_back_kb()
    title = dbmanager.del_cart(message.chat.id)
    bot.send_message(message.chat.id, f'<b>{title}</b>\n', parse_mode='HTML', reply_markup=kb)


# Описание в Reply кнопки "Настройки"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == START_KB['settings'])
def hello(message):
    kb = kb_shop.settings_kb()
    kb_shop.set_prev_kb(kb)
    bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)


# Описание в Reply кнопки "Настройки" --> "Имя"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == SETTINGS_KB['name'])
def change_name(message):
    kb = kb_shop.go_back_kb()
    status_id = DBManager.check_status(message.chat.id)
    name = DBManager.check_data(message.chat.id, temp_fname=True)

    if name and status_id >= 2:
        msg_name = bot.send_message(message.chat.id, f'Вы зарегистрированы как:{name}\nВведите новое имя:',
                                    reply_markup=kb)
        bot.register_next_step_handler(msg_name, create_name)
    else:
        msg_name = bot.send_message(message.chat.id, f'Ваше старое имя:{message.chat.first_name}\nВведите новое имя:',
                                    reply_markup=kb)
        bot.register_next_step_handler(msg_name, create_name)


def create_name(message):
    if message.text == HOME_BACK_KB['home'] or message.text == HOME_BACK_KB['back']:
        kb = kb_shop.start_kb()
        bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=kb)
    else:
        if DBManager.create_data(message.chat.id, temp_new_name=message.text):
            bot.send_message(message.chat.id, f'Вы зарегистрированы как:{message.text}')
            kb = kb_shop.settings_kb()
            kb_shop.set_prev_kb(kb)
            bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)
            return


# Описание в Reply кнопки "Настройки" --> "Моб."
@bot.message_handler(content_types=['text'], func=lambda call: call.text == SETTINGS_KB['phone'])
def change_phone(message):
    kb = kb_shop.go_back_kb()
    status_id = DBManager.check_status(message.chat.id)
    phone = DBManager.check_data(message.chat.id, temp_phonenumber=True)

    if status_id == 1:
        bot.send_message(message.chat.id, f'Сначала введите свое имя, а потом номер телефона:')
        kb = kb_shop.settings_kb()
        kb_shop.set_prev_kb(kb)
        bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)
        return

    if phone and status_id >= 2:
        msg_name = bot.send_message(message.chat.id, f'Ваш телефон:{phone}\nВведите новый телефон:', reply_markup=kb)
        bot.register_next_step_handler(msg_name, create_phone)
    else:
        msg_name = bot.send_message(message.chat.id, f'Введите номер телефона:', reply_markup=kb)
        bot.register_next_step_handler(msg_name, create_phone)


def create_phone(message):
    if message.text == HOME_BACK_KB['home'] or message.text == HOME_BACK_KB['back']:
        kb = kb_shop.start_kb()
        bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=kb)
    else:
        if DBManager.create_data(message.chat.id, temp_phonenumber=str(message.text)):
            bot.send_message(message.chat.id, f'Ваш номер:{message.text} зарегистрирован')
            kb = kb_shop.settings_kb()
            bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)


# Описание в Reply кнопки "Настройки" --> "Адрес"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == SETTINGS_KB['address'])
def change_address(message):
    kb = kb_shop.go_back_kb()
    status_id = DBManager.check_status(message.chat.id)
    address = DBManager.check_data(message.chat.id, temp_address=True)

    if status_id == 1:
        bot.send_message(message.chat.id, f'Сначала введите свое имя, а потом адрес:', reply_markup=kb)
        kb = kb_shop.settings_kb()
        kb_shop.set_prev_kb(kb)
        bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)
        return

    if status_id >= 2:

        if address:
            msg_name = bot.send_message(message.chat.id, f'Ваш адрес:{address}\nВведите новый адрес:', reply_markup=kb)
            bot.register_next_step_handler(msg_name, create_address)
        else:
            msg_name = bot.send_message(message.chat.id, f'Введите адрес доставки:', reply_markup=kb)
            bot.register_next_step_handler(msg_name, create_address)


def create_address(message):
    if message.text == HOME_BACK_KB['home'] or message.text == HOME_BACK_KB['back']:
        kb = kb_shop.start_kb()
        bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=kb)
    else:
        if DBManager.create_data(message.chat.id, temp_address=message.text):
            bot.send_message(message.chat.id, f'Ваш адрес доставки:{message.text}')
            kb = kb_shop.settings_kb()
            kb_shop.set_prev_kb(kb)
            bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)


# Описание в Reply кнопки "Настройки" --> "email"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == SETTINGS_KB['email'])
def change_email(message):
    kb = kb_shop.go_back_kb()
    status_id = DBManager.check_status(message.chat.id)

    if status_id == 1:
        bot.send_message(message.chat.id, f'Сначала введите свое имя, а потом емейл:')
        kb = kb_shop.settings_kb()
        kb_shop.set_prev_kb(kb)
        bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)
        return

    if status_id >= 2:
        address = DBManager.check_data(message.chat.id, temp_email=True)
        if address:
            msg_name = bot.send_message(message.chat.id, f'Ваш емейл:{address}\nВведите емейл:', reply_markup=kb)
            bot.register_next_step_handler(msg_name, create_email)
        else:
            msg_name = bot.send_message(message.chat.id, f'Введите почтовый адрес:', reply_markup=kb)
            bot.register_next_step_handler(msg_name, create_email)


def create_email(message):
    if message.text == HOME_BACK_KB['home'] or message.text == HOME_BACK_KB['back']:
        kb = kb_shop.start_kb()
        bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=kb)
    else:
        if DBManager.create_data(message.chat.id, temp_email=message.text):
            bot.send_message(message.chat.id, f'Ваш почтовый адрес:{message.text}')
            kb = kb_shop.settings_kb()
            kb_shop.set_prev_kb(kb)
            bot.send_message(message.chat.id, "Выберите настройки, которые хотите поменять:", reply_markup=kb)


# Описание в Reply кнопки "Настройки" --> "Помощь"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == START_KB['help'])
def hello(message):
    bot.send_message(message.chat.id, "<b>Наши роуты:</b>\n<b>/tg/category/all</b>\n<b>/tg/products/all</b>\n"
                                      "<b>/tg/tempdata/all</b>\n<b>/tg/users/all</b>\n<b>/tg/admin/all</b>\n"
                                      "<b>/tg/status/all</b>\n<b>Доступ в админку:</b>\n<b>/tg/admin/</b>",
                     parse_mode='HTML')


# Описание в Reply кнопки "Поиск товара"
@bot.message_handler(content_types=['text'], func=lambda call: call.text == START_KB['search'])
def title_search(message):
    kb = kb_shop.go_back_kb()
    msg = bot.send_message(message.chat.id, "Введите название товара для поиска", reply_markup=kb)
    bot.register_next_step_handler(msg, search_product)
    return


def search_product(message):
    title = message.text
    search_title = re.compile(f'[\w\s]*{title}[\w\s]*', re.IGNORECASE)
    for product in Products.objects(title=search_title):
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text=f'Добавить в корзину',
                                      callback_data=f'{add_product}{separator}{product.id}')
        kb.add(button)

        bot.send_photo(message.chat.id, product.image.get(), caption=f'<b>Title:{product.title}</b>\n'
        f'<b>Description:</b>{product.description}\n<b>Price:</b><s>{product.price}</s>\n'
        f'<b>Discount price:</b>{product.get_discount_price()}\n<b>Product weight:</b>'
        f'{product.attributes.weight}\n'
        f'<b>Product(WxHxD):</b>{product.attributes.width}x{product.attributes.height}x'
        f'{product.attributes.depth}', parse_mode='HTML', reply_markup=kb)

        time.sleep(1)
    return


def start_bot():
    import time
    bot.remove_webhook()
    time.sleep(2)
    # bot.set_webhook()
    # bot.polling()
    bot.set_webhook(WEBHOOK_URL,
                    certificate=open('webhook_cert.pem', 'r')
                    )

