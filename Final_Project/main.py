from webshop.api import client
from webshop.bot.main import start_bot
from multiprocessing import Process

from flask import Flask


app = Flask(__name__)


def main_server():
    client.start_client()


def main_client():
    start_bot()


if __name__ == "__main__":
    p1 = Process(target=main_server)
    p1.start()
    p2 = Process(target=main_client)
    p2.start()
    p1.join()
    p2.join()

    # main_server()
    # main_client()
#    app.run(debug=True)
