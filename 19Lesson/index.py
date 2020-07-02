from flask import Flask
from webshop.bot.main import start_bot

app = Flask(__name__)

app.run(debug=True)
start_bot()