from telebot import TeleBot
from app.bot_manager import DBManager

bot = TeleBot("1209000481:AAH1fS_aqzpegkrcsvtMlV2ZfmUooKwXUK4")

dbmanager = DBManager()


@bot.message_handler(commands=['start'])
def hello(message):
    msg = bot.send_message(message.chat.id, 'Здравствуйте, введите свои ФИО(Через пробел, без доп символов).')
    bot.register_next_step_handler(msg, fio)


def fio(message):
    if not dbmanager.get_fio(message.text):
        msg = bot.send_message(message.chat.id, 'Введите еще раз ФИО(корректно)')
        bot.register_next_step_handler(msg, fio)
        return
    msg = bot.send_message(message.chat.id, 'Введите номер телефона, без пробелов и доп символов')
    bot.register_next_step_handler(msg, phone_number)


def phone_number(message):
    if not dbmanager.get_phone(message.text):
        msg = bot.send_message(message.chat.id, 'Введите еще раз телефон(корректно)')
        bot.register_next_step_handler(msg, phone_number)
        return
    msg = bot.send_message(message.chat.id, 'Введите email')
    bot.register_next_step_handler(msg, email)


def email(message):
    if not dbmanager.get_email(message.text):
        msg = bot.send_message(message.chat.id, 'Введите еще раз emeil(корректно)')
        bot.register_next_step_handler(msg, email)
        return
    msg = bot.send_message(message.chat.id, 'Введите address')
    bot.register_next_step_handler(msg, address)


def address(message):
    if not dbmanager.get_address(message.text):
        msg = bot.send_message(message.chat.id, 'Введите еще раз address(корректно)')
        bot.register_next_step_handler(msg, address)
        return
    msg = bot.send_message(message.chat.id, 'Введите примечание')
    bot.register_next_step_handler(msg, comments)


def comments(message):
    if not dbmanager.get_comment(message.text):
        msg = bot.send_message(message.chat.id, 'Введите еще раз примечание(корректно)')
        bot.register_next_step_handler(msg, comments)
        return
    bot.send_message(message.chat.id, 'Спасибо, ваши данные проверены и записаны')


bot.polling()