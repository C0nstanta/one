from flask import Flask, abort, request
from webshop.bot import config

from telebot import TeleBot
from telebot.types import Update


app = Flask(__name__)
bot = TeleBot(config.TOKEN)

@app.route(config.WEBHOOK_PATH, methods=['GET', 'POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


def start_bot():
    import time
    bot.remove_webhook()
    time.sleep(1)
    # bot.set_webhook()
    # res = bot.get_webhook_info()
    # print(res)
    # bot.polling()
    bot.set_webhook(config.WEBHOOK_URL,
                    certificate=open('webhook_cert.pem', 'r')
                    )


if __name__ == "__main__":
    start_bot()
    app.run(port=5000, debug=True)
