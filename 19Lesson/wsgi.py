from webshop.bot import config
from webshop.bot.main import start_bot, bot
from flask import Flask, request, abort
from telebot.types import Update


app = Flask(__name__)

# @app.route(config.WEBHOOK_PATH, methods=['POST'])
# def webhook():
#     if request.headers.get('content-type') == 'application/json':
#         json_string = request.get_data().decode('utf-8')
#         update = Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#     else:
#         abort(403)

#
# if __name__ == '__main__':
start_bot()
    # app.run(port=5000, debug=True)