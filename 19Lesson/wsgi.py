from webshop.bot.main import start_bot
from flask import Flask

app = Flask(__name__)
start_bot()