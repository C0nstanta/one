from webshop.bot.main import start_bot
from flask import Flask, abort, request
from telebot.types import Update
from webshop.bot.main import bot
from webshop.bot import config


app = Flask(__name__)


@app.route(config.WEBHOOK_PATH, methods=['GET', 'POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


start_bot()
app.run(port=5000, debug=True)
