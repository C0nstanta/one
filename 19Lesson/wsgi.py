from webshop.bot.main import start_bot, app
from flask import Flask


app.run(port=5000, debug=True)
start_bot()
