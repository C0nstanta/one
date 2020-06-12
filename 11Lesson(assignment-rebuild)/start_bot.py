"""
Реализована проверка состояния юзера, зашедшего на бота.
При заходе бот отправляет message.chat.id в базу и менеджер базы смотрит, есть ли такой пользователь. Если есть -
проверяет его статус и дальше согласно этого статуса отправляет на какой то блок кода для прохождения авторизации.
Если статуса нет - присваивается по умолчанию 1 и начинается процедура прохождения авторизации.
Таблица статусов:
1 - Начало авторизации. Ввод ФИО(потом распарсиваем)
2 - Вводим номер телефона
3 - Вводим емейл
4 - Вводим адрес
5 - Примечание
6 - Полностью прошел авторизацию и запсиан в базу

Но если бот крашится - промежуточные данные пользователя тоже нужно сохранять. А то статус есть, а данных нет..
Создаем коллекцию промежуточных результатов. После создания пользователя - его документ из промежуточных
результатов удаляется.
"""


from telebot import TeleBot
from app.bot_manager import DBManager

bot = TeleBot("1209000481:AAH1fS_aqzpegkrcsvtMlV2ZfmUooKwXUK4")

dbmanager = DBManager()


@bot.message_handler(commands=['start'])
def hello(message):
    status_id = dbmanager.check_status(message.chat.id)

    if status_id == 0:
        bot.send_message(message.chat.id, 'Вы забанены.).')
        return

    if status_id == 1:
        msg = bot.send_message(message.chat.id, 'Здравствуйте, введите свои ФИО(Через пробел, без доп символов).')
        bot.register_next_step_handler(msg, fio)

    if status_id == 2:
        dbmanager.temp_data(message.chat.id, status_id)
        msg = bot.send_message(message.chat.id, 'Введите номер телефона, без пробелов и доп символов')
        bot.register_next_step_handler(msg, phone_number)

    if status_id == 3:
        dbmanager.temp_data(message.chat.id, status_id)
        msg = bot.send_message(message.chat.id, 'Введите email')
        bot.register_next_step_handler(msg, email)

    if status_id == 4:
        dbmanager.temp_data(message.chat.id, status_id)
        msg = bot.send_message(message.chat.id, 'Введите address')
        bot.register_next_step_handler(msg, address)

    if status_id == 5:
        dbmanager.temp_data(message.chat.id, status_id)
        msg = bot.send_message(message.chat.id, 'Введите примечание')
        bot.register_next_step_handler(msg, comments)

    if status_id == 6:
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')


def fio(message):
    if not dbmanager.get_fio(message.text, message.chat.id):
        msg = bot.send_message(message.chat.id, 'Введите еще раз ФИО(корректно)')
        bot.register_next_step_handler(msg, fio)
        return

    status_id = dbmanager.check_status(message.chat.id)
    if status_id == 2:
        msg = bot.send_message(message.chat.id, 'Введите номер телефона, без пробелов и доп символов')
        bot.register_next_step_handler(msg, phone_number)


def phone_number(message):
    if not dbmanager.get_phone(message.text, message.chat.id):
        msg = bot.send_message(message.chat.id, 'Введите еще раз телефон(корректно)')
        bot.register_next_step_handler(msg, phone_number)
        return

    status_id = dbmanager.check_status(message.chat.id)
    if status_id == 3:
        msg = bot.send_message(message.chat.id, 'Введите email')
        bot.register_next_step_handler(msg, email)


def email(message):
    if not dbmanager.get_email(message.text, message.chat.id):
        msg = bot.send_message(message.chat.id, 'Введите еще раз emeil(корректно)')
        bot.register_next_step_handler(msg, email)
        return

    status_id = dbmanager.check_status(message.chat.id)
    if status_id == 4:
        msg = bot.send_message(message.chat.id, 'Введите address')
        bot.register_next_step_handler(msg, address)


def address(message):
    if not dbmanager.get_address(message.text, message.chat.id):
        msg = bot.send_message(message.chat.id, 'Введите еще раз address(корректно)')
        bot.register_next_step_handler(msg, address)
        return

    status_id = dbmanager.check_status(message.chat.id)
    if status_id == 5:
        msg = bot.send_message(message.chat.id, 'Введите примечание')
        bot.register_next_step_handler(msg, comments)


def comments(message):
    if not dbmanager.get_comment(message.text, message.chat.id):
        msg = bot.send_message(message.chat.id, 'Введите еще раз примечание(корректно)')
        bot.register_next_step_handler(msg, comments)
        return

    status_id = dbmanager.check_status(message.chat.id)
    if status_id == 6:
        dbmanager.temp_drop_doc(message.chat.id)
        bot.send_message(message.chat.id, 'Спасибо, ваши данные проверены и записаны')


bot.polling()