#TODO
# Создать бот для поиска статей на википедии.
# При входе, бот запрашивает пользователя ввести имя статьи.
# Далее бот осуществляет этот поиск на википедии, в случае отстутвия выводит соотвествующие сообщение, а если
# статья найдена выводит на экран текст.
# -------------------------------------------
# Скрипт работает как телеграм бот. Для запуска вводим /start
# Далее вводим запрос, который бот отправляет через request на wikipedia.org
# Скрипт парсит всю информацию по данному запросу в вики и выдает ее назад через
# бота.
# Обработка контекста из вики идет с помощью BeautifulSoup.
# Так - как статьи по запросам очень часто отличаются своим построением и структурой, в папку
# app/testhtml/ записываются файлы в html формате(обрезанные) и text для дальнейшей "настройки", если вдруг
# не устраивает выдача.
# Текст из Вики выдается в полном объеме, если размер сообщения больше 4096, ждем 1 секунду и выдаем следующую
# часть текста.
from telebot import TeleBot
from app.search_engine import SearchWiki
from config import TOKEN
import time

bot = TeleBot(TOKEN)

wikigo = SearchWiki()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введите пожалуйста запрос ")
    print(message.text)


@bot.message_handler(content_types=['text'])
def search_func(message):
    print(message.text)
    res = wikigo.wiki_search(message.text)
    if len(res) > 4096:
        for x in range(0, len(res), 4096):
            bot.send_message(message.chat.id, res[x:x + 4096], parse_mode= 'HTML')
            time.sleep(1)
    else:
        bot.send_message(message.chat.id, res)


if __name__ == "__main__":
    bot.polling()
